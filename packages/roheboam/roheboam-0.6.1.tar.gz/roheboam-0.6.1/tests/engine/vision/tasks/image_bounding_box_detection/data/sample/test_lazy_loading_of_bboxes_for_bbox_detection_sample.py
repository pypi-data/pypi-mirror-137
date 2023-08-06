import numpy as np

from roheboam.engine.testing.image_bounding_box_detection import create_black_image_data, create_random_labels_data
from roheboam.engine.vision.tasks.image_bounding_box_detection.data import ImageBoundingBoxDetectionSample


def test_lazy_loading_of_bboxes_for_bounding_box_detection_sample():
    # Setup sample
    image_data = create_black_image_data(width=512, height=512, n_channels=3)
    bboxes_data = np.array(
        [
            [0.479492, 0.688771, 0.955609, 0.5955],
            [0.736516, 0.247188, 0.498875, 0.476417],
            [0.637063, 0.732938, 0.494125, 0.510583],
            [0.339438, 0.418896, 0.678875, 0.7815],
            [0.646836, 0.132552, 0.118047, 0.096937],
            [0.773148, 0.129802, 0.090734, 0.097229],
            [0.668297, 0.226906, 0.131281, 0.146896],
            [0.642859, 0.079219, 0.148063, 0.148062],
        ]
    )
    labels_data = create_random_labels_data(n_labels=8, n_classes=10)
    sample = ImageBoundingBoxDetectionSample.create(image_data=image_data, bboxes_data=bboxes_data, labels_data=labels_data, bboxes_format="YOLO")

    # Make sure that it is in YOLO format
    assert sample.bboxes_format == "YOLO"
    assert (
        sample.bboxes.data
        == np.array(
            [
                [0.479492, 0.688771, 0.955609, 0.5955],
                [0.736516, 0.247188, 0.498875, 0.476417],
                [0.637063, 0.732938, 0.494125, 0.510583],
                [0.339438, 0.418896, 0.678875, 0.7815],
                [0.646836, 0.132552, 0.118047, 0.096937],
                [0.773148, 0.129802, 0.090734, 0.097229],
                [0.668297, 0.226906, 0.131281, 0.146896],
                [0.642859, 0.079219, 0.148063, 0.148062],
            ]
        )
    ).all()

    # Convert lazily to PASCAL_VOC
    sample.convert_to_pascal_voc_bboxes(lazy=True)
    assert sample._bboxes_format == "YOLO"

    # See if it is converted to PASCAL_VOC when accessed
    assert np.all(
        sample.bboxes.data
        == np.array(
            [
                [0.8639999999999759, 200.202752, 490.135808, 505.098752],
                [249.38419199999998, 4.597504000000001, 504.80819199999996, 248.523008],
                [199.68025600000004, 244.555008, 452.672256, 505.973504],
                [0.00025600000000736145, 14.410752000000002, 347.584256, 414.538752],
                [300.96, 43.050752, 361.400064, 92.682496],
                [372.62387199999995, 41.568, 419.07968, 91.349248],
                [308.560128, 78.57049599999999, 375.776, 153.781248],
                [291.23967999999996, 2.656255999999999, 367.047936, 78.464],
            ]
        )
    )
    assert sample.bboxes_format == "PASCAL_VOC"
