"""genft

usage: genft [-hv] (-d MIXDB) [-i MIXID] [-o OUTPUT]

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -d MIXDB, --mixdb MIXDB         Mixture database JSON file.
    -i MIXID, --mixid MIXID         Mixtures to include (using Python slice notation). [default: :].
    -o OUTPUT, --output OUTPUT      Output HDF5 file.

Generate a SonusAI feature/truth file from a SonusAI mixture database.

Inputs:
    MIXDB       A SonusAI mixture database JSON file.
    MIXID       Mixtures to include (uses Python slice notation, i.e., start:stop:step).

Outputs:
    OUTPUT.h5   A SonusAI feature HDF5 file (containing 'feature' and 'truth_f' datasets).
    genft.log

"""

import json
from copy import deepcopy
from datetime import timedelta
from os.path import exists
from os.path import splitext
from typing import List
from typing import Union

import h5py
import numpy as np
from docopt import docopt
from pyaaware import FeatureGenerator
from pyaaware import ForwardTransform
from tqdm import tqdm

import sonusai
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.mixture import apply_augmentation
from sonusai.mixture import build_noise_audio_db
from sonusai.mixture import build_target_audio_db
from sonusai.mixture import generate_truth
from sonusai.mixture import get_mixtures_from_mixid
from sonusai.mixture import get_total_class_count
from sonusai.mixture import process_mixture_audio
from sonusai.mixture import truth_reduction
from sonusai.utils import human_readable_size
from sonusai.utils import int16_to_float
from sonusai.utils import trim_docstring


def genft(mixdb: dict,
          mixid: Union[str, List[int]],
          start_offset: int = 0,
          logging: bool = True,
          show_progress: bool = False) -> (np.ndarray, np.ndarray, dict):
    mixdb_out = deepcopy(mixdb)
    mixdb_out['mixtures'] = get_mixtures_from_mixid(mixdb_out['mixtures'], mixid)

    if not mixdb_out['mixtures']:
        logger.error('Error processing mixid: {}; resulted in empty list of mixtures'.format(mixid))
        exit()

    total_samples = sum([sub['samples'] for sub in mixdb_out['mixtures']])

    fft = ForwardTransform(N=mixdb_out['frame_size'] * 4, R=mixdb_out['frame_size'])
    fg = FeatureGenerator(frame_size=mixdb_out['frame_size'],
                          feature_mode=mixdb_out['feature'],
                          num_classes=mixdb_out['num_classes'],
                          truth_mutex=mixdb_out['truth_mutex'])

    transform_frames = total_samples // mixdb_out['frame_size']
    # TODO
    #  Update feature_frames with start_offset
    feature_frames = total_samples // mixdb_out['feature_step_samples']

    feature = np.empty((feature_frames, fg.stride, fg.num_bands), dtype=np.single)
    truth_f = np.empty((feature_frames, fg.num_classes), dtype=np.single)

    if logging:
        logger.info('')
        logger.info('Found {} mixtures to process'.format(len(mixdb_out['mixtures'])))
        logger.info('{} samples, {} transform frames, {} feature frames'.format(total_samples, transform_frames,
                                                                                feature_frames))

    noise_audios = build_noise_audio_db(mixdb_out)
    target_audios = build_target_audio_db(mixdb_out)

    i_sample_offset = 0
    i_frame_offset = 0
    o_frame_offset = 0
    feature_frame = 0
    for mixture_record in tqdm(mixdb_out['mixtures'], desc='Processing', disable=not show_progress):
        noise_audio, target_audio = process_mixture_audio(i_frame_offset=i_frame_offset,
                                                          i_sample_offset=i_sample_offset,
                                                          o_frame_offset=o_frame_offset,
                                                          mixdb=mixdb_out,
                                                          mixture_record=mixture_record,
                                                          target_audios=target_audios,
                                                          noise_audios=noise_audios)

        mixture_audio = np.array(target_audio + noise_audio, dtype=np.int16)

        truth = generate_truth(mixdb=mixdb_out, mixture_record=mixture_record, target_audio=target_audio)

        for offset in range(0, mixture_record['samples'], mixdb_out['frame_size']):
            mixture_fd = fft.execute(int16_to_float(mixture_audio[offset:offset + mixdb_out['frame_size']]))
            fg.execute(mixture_fd,
                       truth_reduction(truth[:, offset:offset + mixdb_out['frame_size']],
                                       mixdb_out['truth_reduction_function']))
            if fg.eof():
                # start_offset is used when generating one batch at a time and makes it
                # possible to preserve the mixture data sequence across batch boundaries
                if start_offset != 0:
                    start_offset -= 1
                else:
                    feature[feature_frame] = np.reshape(fg.feature(), (fg.stride, fg.num_bands))
                    truth_f[feature_frame] = fg.truth()
                    feature_frame += 1

        fft.reset()
        fg.reset()

        i_sample_offset += mixture_record['samples']
        i_frame_offset += mixture_record['samples'] // mixdb_out['frame_size']
        o_frame_offset += mixture_record['samples'] // mixdb_out['feature_step_samples']

    mixdb_out['class_count'] = get_total_class_count(mixdb_out)

    duration = total_samples / sonusai.mixture.sample_rate
    if logging:
        logger.info('')
        logger.info('Duration: {}'.format(timedelta(seconds=duration)))
        logger.info('feature:  {}'.format(human_readable_size(feature.nbytes, 1)))
        logger.info('truth_f:  {}'.format(human_readable_size(truth_f.nbytes, 1)))

    return feature, truth_f, mixdb_out


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.version(), options_first=True)

        verbose = args['--verbose']
        mixdb_name = args['--mixdb']
        mixid = args['--mixid']
        output_name = args['--output']

        if not output_name:
            output_name = splitext(mixdb_name)[0] + '.h5'

        log_name = 'genft.log'
        create_file_handler(log_name)
        update_console_handler(verbose)
        initial_log_messages('genft')

        if not exists(mixdb_name):
            logger.error('{} does not exist'.format(mixdb_name))
            exit()

        with open(mixdb_name, encoding='utf-8') as f:
            mixdb = json.load(f)

        feature, truth_f, mixdb_out = genft(mixdb=mixdb,
                                            mixid=mixid,
                                            show_progress=True)

        with h5py.File(output_name, 'w') as f:
            f.attrs['mixdb'] = json.dumps(mixdb_out)
            f.create_dataset(name='feature', data=feature)
            f.create_dataset(name='truth_f', data=truth_f)
            logger.info('Wrote {}'.format(output_name))

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()


if __name__ == '__main__':
    main()
