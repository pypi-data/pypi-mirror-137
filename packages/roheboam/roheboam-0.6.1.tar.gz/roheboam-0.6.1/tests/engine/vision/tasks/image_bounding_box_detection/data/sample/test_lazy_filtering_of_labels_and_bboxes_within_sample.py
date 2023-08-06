import numpy as np
import pytest

from roheboam.engine.testing.image_bounding_box_detection import create_black_image_data, create_random_yolo_bboxes_data
from roheboam.engine.vision.tasks.image_bounding_box_detection.data import ImageBoundingBoxDetectionSample, create_image_bboxes_detection_sample


def test_lazy_filtering_of_labels_and_bboxes_within_sample_with_data():
    # Setup sample
    image_data = create_black_image_data(width=128, height=128, n_channels=3)
    labels_data = np.array([0, 1, 1, 2, 2, 2, 3, 3])
    bboxes_data = create_random_yolo_bboxes_data(n_bboxes=len(labels_data))
    sample = ImageBoundingBoxDetectionSample.create(image_data=image_data, bboxes_data=bboxes_data, labels_data=labels_data, bboxes_format="YOLO")
    sample.filter_labels_and_bboxes_to_keep(labels_to_keep=[0, 1], lazy=True)

    # Test that it has not been filtered yet
    # (Kind of bad as we are exposing implementation details)
    assert np.all(sample._labels.data == labels_data)
    assert np.all(sample._bboxes.data == bboxes_data)

    # Test that when the labels are filtered when it is accessed
    assert np.all(sample.labels.data == np.array([0, 1, 1]))

    # Test that the bboxes stay the same when the labels are filtered, this is inconsistent
    # but we need to make this tradeoff so that filtering by samples don't slow down everything
    assert np.all(sample._bboxes.data == bboxes_data)


@pytest.mark.skip()
def test_lazy_filtering_of_labels_and_bboxes_within_sample_with_data_for_5000_samples_is_under_1_second():
    samples = []
    for _ in range(5000):
        image_data = create_black_image_data(width=32, height=32, n_channels=3)
        labels_data = np.array([0, 1, 1, 2, 2, 2, 3, 3])
        bboxes_data = create_random_yolo_bboxes_data(n_bboxes=len(labels_data))
        sample = ImageBoundingBoxDetectionSample.create(
            image_data=image_data, bboxes_data=bboxes_data, labels_data=labels_data, bboxes_format="YOLO"
        )
        sample.filter_labels_and_bboxes_to_keep(labels_to_keep=[0, 1], lazy=True)
        samples.append(sample)


@pytest.mark.skip()
def test_lazy_filtering_of_labels_and_bboxes_within_sample_with_data_for_5000_samples_is_under_1_second_for_create_wrapper():
    samples = []
    for _ in range(5000):
        image_data = create_black_image_data(width=32, height=32, n_channels=3)
        labels_data = np.array([0, 1, 1, 2, 2, 2, 3, 3])
        bboxes_data = create_random_yolo_bboxes_data(n_bboxes=len(labels_data))
        sample = create_image_bboxes_detection_sample(
            image_data=image_data, bboxes_data=bboxes_data, labels_data=labels_data, bboxes_format="YOLO", labels_to_keep=[0, 1]
        )
        samples.append(sample)
