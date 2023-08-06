import numpy as np

from sonusai import logger
from sonusai.mixture import apply_augmentation
from sonusai.mixture import get_next_noise
from sonusai.mixture import get_noise_audio_from_db
from sonusai.mixture import get_target_audio_from_db


def process_mixture_audio(i_frame_offset: int,
                          i_sample_offset: int,
                          o_frame_offset: int,
                          mixdb: dict,
                          mixture_record: dict,
                          target_audios: list,
                          noise_audios: list) -> (np.ndarray, np.ndarray):
    if mixture_record['samples'] % mixdb['frame_size'] != 0:
        logger.error('Number of samples in mixture is not a multiple of {}'.format(mixdb['frame_size']))
        exit()
    target_file_index = mixture_record['target_file_index']
    target_augmentation = mixdb['target_augmentations'][mixture_record['target_augmentation_index']]
    target_audio = apply_augmentation(audio_in=get_target_audio_from_db(target_audios, target_file_index),
                                      augmentation=target_augmentation,
                                      length_common_denominator=mixdb['feature_step_samples'],
                                      dither=mixdb['dither'])
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

    target_audio = np.int16(np.single(target_audio) * mixture_record['target_snr_gain'])
    noise_audio = np.int16(np.single(noise_audio) * mixture_record['noise_snr_gain'])

    return noise_audio, target_audio
