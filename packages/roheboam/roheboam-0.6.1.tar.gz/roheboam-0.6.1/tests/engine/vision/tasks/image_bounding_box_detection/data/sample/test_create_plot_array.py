import numpy as np
import torch

from roheboam.engine.testing.image_bounding_box_detection import create_black_image_data, create_random_labels_data, create_random_yolo_bboxes_data
from roheboam.engine.vision.tasks.image_bounding_box_detection.data import ImageBoundingBoxDetectionSample


def test_sample_pascal_voc_bboxes_from_coco_format():
    labels_data = create_random_labels_data(n_labels=1, n_classes=3)
    image_data = create_black_image_data(width=1000, height=1000, n_channels=3)
    coco_format_bboxes_data = np.array([[559, 213, 50, 32]])
    sample = ImageBoundingBoxDetectionSample.create(
        image_data=image_data, bboxes_data=coco_format_bboxes_data, labels_data=labels_data, bboxes_format="COCO"
    )

    assert np.all(sample.pascal_voc_bboxes == np.array([[559, 213, 609, 245]]))
