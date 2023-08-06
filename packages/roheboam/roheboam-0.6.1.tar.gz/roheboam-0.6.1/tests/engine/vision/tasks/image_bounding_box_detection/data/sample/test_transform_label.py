import numpy as np
import pytest

from roheboam.engine.testing.image_bounding_box_detection import create_black_image_data, create_random_yolo_bboxes_data
from roheboam.engine.vision.tasks.image_bounding_box_detection.data import ImageBoundingBoxDetectionSample


def test_transform_labels_within_sample_with_data():
    image_data = create_black_image_data(width=128, height=128, n_channels=3)
    labels_data = np.array([0, 11, 112, "hello"])
    bboxes_data = create_random_yolo_bboxes_data(n_bboxes=len(labels_data))
    sample = ImageBoundingBoxDetectionSample.create(image_data=image_data, bboxes_data=bboxes_data, labels_data=labels_data, bboxes_format="YOLO")

    # Here we have to use a str for the integers since numpy will convert the ints to str
    label_map = {"0": 0, "11": 1, "112": 2, "hello": 3}

    sample.transform_labels(label_map, lazy=False)

    assert np.all(np.array(sample.labels.data) == np.array([0, 1, 2, 3]))


def test_lazy_transform_labels_within_sample_with_data():
    # Setup sample
    image_data = create_black_image_data(width=128, height=128, n_channels=3)
    labels_data = np.array(["0", "11", "112", "hello"])
    bboxes_data = create_random_yolo_bboxes_data(n_bboxes=len(labels_data))
    sample = ImageBoundingBoxDetectionSample.create(image_data=image_data, bboxes_data=bboxes_data, labels_data=labels_data, bboxes_format="YOLO")

    # Here we have to use a str for the integers since numpy will convert the ints to str
    label_map = {"0": 0, "11": 1, "112": 2, "hello": 3}

    sample.transform_labels(label_map, lazy=True)

    assert np.all(np.array(sample._labels.data) == np.array(["0", "11", "112", "hello"]))
    assert np.all(np.array(sample.labels.data) == np.array([0, 1, 2, 3]))


def test_lazy_filter_then_transform_label_within_sample_with_data():
    # Setup sample
    image_data = create_black_image_data(width=128, height=128, n_channels=3)
    labels_data = np.array(["0", "11", "112", "hello"])
    bboxes_data = create_random_yolo_bboxes_data(n_bboxes=len(labels_data))
    sample = ImageBoundingBoxDetectionSample.create(image_data=image_data, bboxes_data=bboxes_data, labels_data=labels_data, bboxes_format="YOLO")

    # Here we have to use a str for the integers since numpy will convert the ints to str
    label_map = {"11": 1, "112": 2}

    sample.filter_labels_and_bboxes_to_keep(["11", "112"], lazy=True)
    sample.transform_labels(label_map, lazy=True)

    assert np.all(np.array(sample._labels.data) == np.array(["0", "11", "112", "hello"]))
    assert np.all(np.array(sample.labels.data) == np.array([1, 2]))
