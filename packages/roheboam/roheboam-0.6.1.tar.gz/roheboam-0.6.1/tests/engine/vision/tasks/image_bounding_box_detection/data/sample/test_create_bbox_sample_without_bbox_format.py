import numpy as np

from roheboam.engine.testing.image_bounding_box_detection import create_black_image_data, create_random_yolo_bboxes_data
from roheboam.engine.vision.tasks.image_bounding_box_detection.data import ImageBoundingBoxDetectionSample


def test_create_bbox_sample_without_bbox_format():

    labels_data = [np.array([0]), np.array([1, 2]), np.array([0, 2])]
    image_data = create_black_image_data(width=128, height=128, n_channels=3)
    bboxes_data = create_random_yolo_bboxes_data(n_bboxes=len(labels_data))

    try:
        ImageBoundingBoxDetectionSample.create(image_data=image_data, bboxes_data=bboxes_data, labels_data=labels_data)
    except AssertionError as e:
        assert str(e) == "Both bboxes and bboxes_format must be defined together, or not defined at all"
    except Exception:
        assert False
