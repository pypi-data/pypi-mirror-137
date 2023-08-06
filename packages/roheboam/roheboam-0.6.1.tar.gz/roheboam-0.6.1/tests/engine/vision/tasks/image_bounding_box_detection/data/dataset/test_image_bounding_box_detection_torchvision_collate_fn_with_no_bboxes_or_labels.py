import torch

from roheboam.engine.testing.image_bounding_box_detection import create_black_image_data, create_random_labels_data, create_random_yolo_bboxes_data
from roheboam.engine.vision.tasks.image_bounding_box_detection.data import (
    ImageBoundingBoxDetectionDatasetV2,
    ImageBoundingBoxDetectionSample,
    image_bounding_box_detection_torchvision_collate_fn,
)


def test_image_bounding_box_detection_torchvision_collate_fn_with_no_bboxes_or_labels():
    labels_data_0 = create_random_labels_data(n_labels=0, n_classes=3)
    image_data_0 = create_black_image_data(width=128, height=128, n_channels=3)
    bboxes_data_0 = create_random_yolo_bboxes_data(n_bboxes=len(labels_data_0))
    sample_0 = ImageBoundingBoxDetectionSample.create(
        image_data=image_data_0, bboxes_data=bboxes_data_0, labels_data=labels_data_0, bboxes_format="YOLO"
    )

    dataset = ImageBoundingBoxDetectionDatasetV2(samples=[sample_0])
    dataset_sample_0 = dataset[0]
    batch = image_bounding_box_detection_torchvision_collate_fn([dataset_sample_0])

    torch.all(batch["images"][0] == torch.from_numpy(image_data_0).float())
    torch.all(batch["targets"][0]["boxes"] == torch.zeros((0, 4), dtype=torch.float32))
    torch.all(batch["targets"][0]["labels"] == torch.zeros((1, 1), dtype=torch.int64))
