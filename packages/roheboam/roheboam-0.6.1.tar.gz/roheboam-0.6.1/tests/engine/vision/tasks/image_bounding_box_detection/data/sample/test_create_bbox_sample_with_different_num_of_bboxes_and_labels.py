import numpy as np

from roheboam.engine.testing.image_bounding_box_detection import create_black_image_data, create_random_yolo_bboxes_data
from roheboam.engine.vision.tasks.image_bounding_box_detection.data import ImageBoundingBoxDetectionSample


def test_create_bbox_sample_with_different_num_of_bboxes_and_labels():

    labels_data = np.array([0])
    image_data = create_black_image_data(width=128, height=128, n_channels=3)
    bboxes_data = create_random_yolo_bboxes_data(n_bboxes=100)

    try:
        ImageBoundingBoxDetectionSample.create(image_data=image_data, bboxes_data=bboxes_data, labels_data=labels_data)
    except AssertionError as e:
        assert str(e) == "The number of bboxes (100) must be the same as the number of labels (1)"
    except Exception:
        assert False
