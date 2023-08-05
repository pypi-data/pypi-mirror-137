"""genmix

usage: genmix [-hv] (-d MIXDB) [-i MIXID] [-o OUTPUT]

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -d MIXDB, --mixdb MIXDB         Mixture database JSON file.
    -i MIXID, --mixid MIXID         Mixtures to include (using Python slice notation). [default: :].
    -o OUTPUT, --output OUTPUT      Output HDF5 file.

Generate a SonusAI mixture file from a SonusAI mixture database.

Inputs:
    MIXDB       A SonusAI mixture database JSON file.
    MIXID       Mixtures to include (uses Python slice notation, i.e., start:stop:step).

Outputs:
    OUTPUT.h5   A SonusAI mixture HDF5 file (containing 'mixture', 'truth_t', 'target', 'noise', and 'segsnr' datasets).
    genmix.log

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
from sonusai.mixture import get_class_count
from sonusai.mixture import get_class_weights_threshold
from sonusai.mixture import get_mixtures_from_mixid
from sonusai.mixture import get_next_noise
from sonusai.mixture import get_noise_audio_from_db
from sonusai.mixture import get_target_audio_from_db
from sonusai.mixture import get_total_class_count
from sonusai.utils import human_readable_size
from sonusai.utils import int16_to_float
from sonusai.utils import trim_docstring


def genmix(mixdb: dict,
           mixid: Union[str, List[int]],
           compute_segsnr: bool = False,
           show_progress: bool = False) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray, dict):
    mixdb_out = deepcopy(mixdb)
    mixdb_out['mixtures'] = get_mixtures_from_mixid(mixdb_out['mixtures'], mixid)

    if not mixdb_out['mixtures']:
        logger.error('Error processing mixid: {}; resulted in empty list of mixtures'.format(mixid))
        exit()

    class_weights_threshold = get_class_weights_threshold(mixdb_out)

    total_samples = sum([sub['samples'] for sub in mixdb_out['mixtures']])

    target = np.empty(total_samples, dtype=np.int16)
    noise = np.empty(total_samples, dtype=np.int16)
    truth_t = np.empty((mixdb_out['num_classes'], total_samples), dtype=np.single)
    if compute_segsnr:
        segsnr = np.empty(total_samples, dtype=np.single)
        fft = ForwardTransform(N=mixdb_out['frame_size'] * 4, R=mixdb_out['frame_size'])
    else:
        segsnr = np.empty(0)

    logger.info('')
    logger.info('Found {} mixtures to process'.format(len(mixdb_out['mixtures'])))
    logger.info('{} samples'.format(total_samples))

    noise_audios = build_noise_audio_db(mixdb_out)
    target_audios = build_target_audio_db(mixdb_out)

    i_sample_offset = 0
    i_frame_offset = 0
    o_frame_offset = 0
    for mixture_record in (tqdm(mixdb_out['mixtures'], desc='Processing') if show_progress else mixdb_out['mixtures']):
        if mixture_record['samples'] % mixdb_out['frame_size'] != 0:
            logger.error('Number of samples in mixture is not a multiple of {}'.format(mixdb_out['frame_size']))
            exit()

        target_file_index = mixture_record['target_file_index']
        target_augmentation = mixdb_out['target_augmentations'][mixture_record['target_augmentation_index']]
        target_audio = apply_augmentation(audio_in=get_target_audio_from_db(target_audios, target_file_index),
                                          augmentation=target_augmentation,
                                          length_common_denominator=mixdb_out['feature_step_samples'],
                                          dither=mixdb_out['dither'])
        if len(target_audio) != mixture_record['samples']:
            logger.error('Number of samples in target does not match database')
            exit()

        noise_file_index = mixture_record['noise_file_index']
        noise_augmentation_index = mixture_record['noise_augmentation_index']
        noise_audio, _ = get_next_noise(offset_in=mixture_record['noise_offset'],
                                        length=mixture_record['samples'],
                                        audio_in=get_noise_audio_from_db(noise_audios,
                                                                         noise_file_index,
                                                                         noise_augmentation_index))

        mixture_record['i_sample_offset'] = i_sample_offset
        mixture_record['i_frame_offset'] = i_frame_offset
        mixture_record['o_frame_offset'] = o_frame_offset

        audio_indices = slice(i_sample_offset, i_sample_offset + len(target_audio))

        target_audio = np.int16(np.single(target_audio) * mixture_record['target_snr_gain'])
        noise_audio = np.int16(np.single(noise_audio) * mixture_record['noise_snr_gain'])

        target[audio_indices] = target_audio
        noise[audio_indices] = noise_audio

        truth_config = deepcopy(mixdb_out['targets'][mixture_record['target_file_index']]['truth_config'])
        truth_config['index'] = mixdb_out['targets'][mixture_record['target_file_index']]['truth_index']
        truth_config['frame_size'] = mixdb_out['frame_size']
        truth_config['num_classes'] = mixdb_out['num_classes']
        truth_config['mutex'] = mixdb_out['truth_mutex']

        if mixture_record['target_gain'] == 0:
            truth = np.zeros((mixdb_out['num_classes'], len(target_audio)), dtype=np.single)
        else:
            truth = generate_truth(
                audio=np.int16(np.single(target_audio) / mixture_record['target_gain']),
                function=mixdb_out['targets'][mixture_record['target_file_index']]['truth_function'],
                config=truth_config)
        truth_t[:, audio_indices] = truth

        mixture_record['class_count'] = get_class_count(
            truth_index=truth_config['index'],
            truth=truth,
            class_weights_threshold=class_weights_threshold)

        if compute_segsnr:
            for offset in range(0, mixture_record['samples'], mixdb_out['frame_size']):
                target_energy = fft.energy(int16_to_float(target_audio[offset:offset + mixdb_out['frame_size']]))
                noise_energy = fft.energy(int16_to_float(noise_audio[offset:offset + mixdb_out['frame_size']]))
                frame_offset = i_sample_offset + offset
                segsnr[frame_offset:frame_offset + mixdb_out['frame_size']] = np.single(target_energy / noise_energy)

        i_sample_offset += mixture_record['samples']
        i_frame_offset += mixture_record['samples'] // mixdb_out['frame_size']
        o_frame_offset += mixture_record['samples'] // mixdb_out['feature_step_samples']

    mixture = np.array(target + noise, dtype=np.int16)

    mixdb_out['class_count'] = get_total_class_count(mixdb_out)

    duration = len(mixture) / sonusai.mixture.sample_rate
    logger.info('')
    logger.info('Duration: {} ([D day[s], ][H]H:MM:SS[.UUUUUU])'.format(timedelta(seconds=duration)))
    logger.info('mixture:  {}'.format(human_readable_size(mixture.nbytes, 1)))
    logger.info('truth_t:  {}'.format(human_readable_size(truth_t.nbytes, 1)))

    return mixture, truth_t, target, noise, segsnr, mixdb_out


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.version(), options_first=True)

        verbose = args['--verbose']
        mixdb_name = args['--mixdb']
        mixid = args['--mixid']
        output_name = args['--output']

        if not output_name:
            output_name = splitext(mixdb_name)[0] + '.h5'

        log_name = 'genmix.log'
        create_file_handler(log_name)
        update_console_handler(verbose)
        initial_log_messages('genmix')

        if not exists(mixdb_name):
            logger.error('{} does not exist'.format(mixdb_name))
            exit()

        with open(mixdb_name, encoding='utf-8') as f:
            mixdb = json.load(f)

        mixture, truth_t, target, noise, segsnr, mixdb_out = genmix(mixdb=mixdb,
                                                                    mixid=mixid,
                                                                    compute_segsnr=True,
                                                                    show_progress=True)

        with h5py.File(output_name, 'w') as f:
            f.attrs['mixdb'] = json.dumps(mixdb_out)
            f.create_dataset(name='mixture', data=mixture)
            f.create_dataset(name='truth_t', data=truth_t)
            f.create_dataset(name='target', data=target)
            f.create_dataset(name='noise', data=noise)
            f.create_dataset(name='segsnr', data=segsnr)
            logger.info('Wrote {}'.format(output_name))

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()


if __name__ == '__main__':
    main()
