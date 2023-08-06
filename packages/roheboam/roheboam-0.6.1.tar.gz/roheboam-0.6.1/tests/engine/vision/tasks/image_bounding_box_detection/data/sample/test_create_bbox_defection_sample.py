import numpy as np

from roheboam.engine.testing.image_bounding_box_detection import create_black_image_data, create_random_yolo_bboxes_data
from roheboam.engine.vision.tasks.image_bounding_box_detection.data import ImageBoundingBoxDetectionSample


def test_create_bboxes_sample_for_yolo_format_from_data():

    labels_data = np.array([0, 1, 2])
    image_data = (create_black_image_data(width=128, height=128, n_channels=3),)
    bboxes_data = create_random_yolo_bboxes_data(n_bboxes=len(labels_data))

    sample = ImageBoundingBoxDetectionSample.create(image_data=image_data, bboxes_data=bboxes_data, labels_data=labels_data, bboxes_format="YOLO")

    assert np.all(sample.image.data == image_data)
    assert np.all(sample.labels.data == labels_data)
    assert np.all(sample.bboxes.data == bboxes_data)
