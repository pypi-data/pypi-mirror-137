import random
from typing import List
from typing import Union

import numpy as np
from tensorflow.keras.utils import Sequence

from sonusai import genft
from sonusai import logger
from sonusai.mixture import get_mixtures_from_mixid
from sonusai.utils import reshape_inputs


class DataGenerator(Sequence):
    """Generates data for Keras"""

    def __init__(self,
                 mixdb: dict,
                 mixid: Union[str, List[int]],
                 batch_size: int,
                 timesteps: int,
                 flatten: bool,
                 add1ch: bool,
                 shuffle: bool = False,
                 chunks: int = 8):
        """Initialization"""
        self.mixdb = mixdb
        self.mixid = mixid
        self.batch_size = batch_size
        self.timesteps = timesteps
        self.flatten = flatten
        self.add1ch = add1ch
        self.shuffle = shuffle
        self.chunks = chunks

        self.mixtures = None
        self.index_map = None
        self.batches_per_epoch = None
        self.features_per_batch = None
        self.feature = None
        self.truth = None
        self.cached_indices = None
        self.cache_misses = []

        self.initialize_mixtures()

    def __len__(self):
        """Denotes the number of batches per epoch"""
        return self.batches_per_epoch

    def __getitem__(self, index):
        """Generate one batch of data"""
        if self.cached_indices is None or index < self.cached_indices[0] or index > self.cached_indices[1]:
            self.fetch_data_for_index(index)

        offset = index - self.cached_indices[0]
        feature, truth, _, _, _, _ = reshape_inputs(feature=self.feature[offset],
                                                    truth=self.truth[offset],
                                                    batch_size=self.batch_size,
                                                    timesteps=self.timesteps,
                                                    flatten=self.flatten,
                                                    add1ch=self.add1ch)

        return feature, truth

    def on_epoch_end(self):
        """Modification of dataset between epochs"""
        if self.shuffle:
            random.shuffle(self.mixid)
            self.initialize_mixtures()

    def get_feature_frames(self, mixtures: list, mixid: Union[str, List[int]]) -> int:
        subset = get_mixtures_from_mixid(mixtures, mixid)
        return sum([sub['samples'] for sub in subset]) // self.mixdb['feature_step_samples']

    def initialize_mixtures(self):
        self.mixtures = get_mixtures_from_mixid(self.mixdb['mixtures'], self.mixid)

        feature_frames = self.get_feature_frames(self.mixtures, ':')
        self.features_per_batch = self.batch_size if self.timesteps == 0 else self.batch_size * self.timesteps
        self.batches_per_epoch = feature_frames // self.features_per_batch

        if self.batches_per_epoch == 0:
            logger.error(
                'Error: dataset only contains {} frames which is not enough to fill a batch size of {}. '
                'Either provide more data or decrease the batch size.'.format(
                    feature_frames, self.features_per_batch))
            exit()

        # Compute mixid and offset for dataset
        # offsets are needed because mixtures are not guaranteed to fall on batch boundaries
        # When fetching a new index that starts in the middle of a sequence of mixtures, the
        # previous feature frame offset must be maintained in order to preserve the correct
        # data sequence.
        offsets = np.cumsum([sub['samples'] for sub in self.mixtures]) // self.mixdb['feature_step_samples'] - 1
        self.index_map = [{} for n in range(self.batches_per_epoch)]
        cur_offset = 0
        prv_id = 0
        for n in range(self.batches_per_epoch):
            mixid = []
            offset = []
            for index in range(n * self.features_per_batch, (n + 1) * self.features_per_batch):
                cur_id = next(idx for idx, val in enumerate(offsets) if val >= index)
                if cur_id != prv_id:
                    cur_offset = 0
                offset.append(cur_offset)
                cur_offset += 1
                prv_id = cur_id
                mixid.append(cur_id)
            mixid = sorted(list(set(mixid)))

            self.index_map[n]['mixid'] = mixid
            self.index_map[n]['offset'] = offset

    def fetch_data_for_index(self, index: int):
        self.cache_misses.append(index)
        mixid = self.index_map[index]['mixid']
        offset = self.index_map[index]['offset'][0]
        # get_feature_frames() does not account for mixture start offset, so the actual number of batches
        # returned from genft() may be less than chunks
        while (self.get_feature_frames(self.mixtures, mixid) // self.features_per_batch) < self.chunks and \
                mixid[-1] < len(self.mixtures) - 1:
            mixid.append(mixid[-1] + 1)

        feature, truth, _ = genft(mixdb=self.mixdb,
                                  mixid=mixid,
                                  start_offset=offset,
                                  logging=False,
                                  show_progress=False)

        features = (feature.shape[0] // self.features_per_batch) * self.features_per_batch
        batches = features // self.features_per_batch

        if batches == 0:
            logger.error(
                'Error: genft returned {} frames which is not enough to fill a batch size of {}. '
                'Either provide more data or decrease the batch size'.format(
                    feature.shape[0], self.features_per_batch))
            exit()

        self.feature = feature[:features].reshape(
            (batches, self.features_per_batch, feature.shape[1], feature.shape[2]))
        self.truth = truth[:features].reshape((batches, self.features_per_batch, truth.shape[1]))

        self.cached_indices = (index, index + batches - 1)

    def get_cache_misses(self):
        return self.cache_misses
