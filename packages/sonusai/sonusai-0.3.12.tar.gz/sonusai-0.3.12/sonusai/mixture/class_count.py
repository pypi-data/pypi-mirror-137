from typing import List

import numpy as np


def get_class_count(truth_index: List[int],
                    truth: np.ndarray,
                    class_weights_threshold: List[float]) -> List[int]:
    class_count = [0] * len(truth_index)
    for idx, cl in enumerate(truth_index):
        truth_sum = int(np.sum(truth[cl - 1,] >= class_weights_threshold[cl - 1]))
        class_count[idx] = truth_sum

    return class_count


def get_total_class_count(mixdb: dict) -> List[int]:
    total_class_count = [0] * mixdb['num_classes']
    for mixture in mixdb['mixtures']:
        for idx, cl in enumerate(mixdb['targets'][mixture['target_file_index']]['truth_index']):
            total_class_count[cl - 1] += int(mixture['class_count'][idx])

    return total_class_count
