import numpy as np

from roheboam.engine.testing.image_bounding_box_detection import create_black_image_data, create_random_yolo_bboxes_data
from roheboam.engine.vision.tasks.image_bounding_box_detection.data import ImageBoundingBoxDetectionSample, filter_image_bboxes_samples_by_labels


def test_filter_image_bboxes_samples_by_labels():
    labels_data_for_samples = [np.array([0]), np.array([1, 2]), np.array([0, 2])]
    samples = []

    for labels_data in labels_data_for_samples:
        samples.append(
            ImageBoundingBoxDetectionSample.create(
                image_data=create_black_image_data(width=128, height=128, n_channels=3),
                bboxes_data=create_random_yolo_bboxes_data(n_bboxes=len(labels_data)),
                labels_data=labels_data,
                bboxes_format="YOLO",
            )
        )

    filtered_samples = filter_image_bboxes_samples_by_labels(samples, labels_to_keep=[0])
    assert len(filtered_samples) == 2
