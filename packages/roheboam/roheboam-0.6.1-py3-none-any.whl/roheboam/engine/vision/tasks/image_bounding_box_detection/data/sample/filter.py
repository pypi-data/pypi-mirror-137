from collections import defaultdict

import numpy as np
from miniutils import parallel_progbar

from .create import create_image_bboxes_detection_sample


def filter_image_bboxes_samples_by_labels(samples, labels_to_keep=None):
    if labels_to_keep is None:
        return samples

    samples_lookup_by_label = create_samples_lookup_by_label(samples)

    filtered_samples = {}
    for label in labels_to_keep:
        for sample in samples_lookup_by_label[label]:
            filtered_samples[id(sample)] = sample
    return np.array([s for s in filtered_samples.values()])


# def filter_image_bboxes_samples_data_by_labels(samples_data, labels_to_keep=None):
#     if labels_to_keep is None:
#         return samples_data

#     samples = parallel_progbar(lambda sample_data: create_image_bboxes_detection_sample(**sample_data), samples_data)
#     samples_lookup_by_label = create_samples_lookup_by_label(samples)

#     filtered_samples = {}
#     for label in labels_to_keep:
#         for sample in samples_lookup_by_label[label]:
#             filtered_samples[id(sample)] = sample
#     filtered_samples = filtered_samples.values()
#     return np.array([s.sample_data_without_loaded_data for s in filtered_samples])


def create_samples_lookup_by_label(samples):
    samples_lookup = defaultdict(list)
    for sample in samples:
        unique_labels = list(set(sample.labels.data))
        for label in unique_labels:
            samples_lookup[label].append(sample)
    return samples_lookup


lookup = {
    "filter_image_bboxes_samples_by_labels": filter_image_bboxes_samples_by_labels,
    # "filter_image_bboxes_samples_data_by_labels": filter_image_bboxes_samples_data_by_labels,
    "create_samples_lookup_by_label": create_samples_lookup_by_label,
}
