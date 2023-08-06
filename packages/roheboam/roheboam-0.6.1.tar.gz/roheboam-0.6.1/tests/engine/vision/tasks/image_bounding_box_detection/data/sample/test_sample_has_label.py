import torch

from roheboam.engine.testing.image_bounding_box_detection import create_black_image_data, create_random_labels_data, create_random_yolo_bboxes_data
from roheboam.engine.vision.tasks.image_bounding_box_detection.data import ImageBoundingBoxDetectionSample


def test_sample_labels_exists_if_length_of_labels_is_zero():
    labels_data = create_random_labels_data(n_labels=0, n_classes=3)
    image_data = create_black_image_data(width=128, height=128, n_channels=3)
    bboxes_data = create_random_yolo_bboxes_data(n_bboxes=len(labels_data))
    sample = ImageBoundingBoxDetectionSample.create(image_data=image_data, bboxes_data=bboxes_data, labels_data=labels_data, bboxes_format="YOLO")
    assert sample.labels_exists


def test_sample_labels_exists_if_length_of_labels_is_greater_than_one():
    labels_data = create_random_labels_data(n_labels=3, n_classes=3)
    image_data = create_black_image_data(width=128, height=128, n_channels=3)
    bboxes_data = create_random_yolo_bboxes_data(n_bboxes=len(labels_data))
    sample = ImageBoundingBoxDetectionSample.create(image_data=image_data, bboxes_data=bboxes_data, labels_data=labels_data, bboxes_format="YOLO")
    assert sample.labels_exists


def test_sample_has_no_labels_if_labels_is_none():
    image_data = create_black_image_data(width=128, height=128, n_channels=3)
    sample = ImageBoundingBoxDetectionSample.create(image_data=image_data, bboxes_data=None, labels_data=None, bboxes_format=None)
    assert sample.labels_exists is False
