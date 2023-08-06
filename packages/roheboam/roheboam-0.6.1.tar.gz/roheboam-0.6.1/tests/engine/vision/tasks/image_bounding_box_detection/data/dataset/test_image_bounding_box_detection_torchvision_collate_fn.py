import torch

from roheboam.engine.testing.image_bounding_box_detection import create_black_image_data, create_random_labels_data, create_random_yolo_bboxes_data
from roheboam.engine.vision.tasks.image_bounding_box_detection.data import (
    ImageBoundingBoxDetectionDatasetV2,
    ImageBoundingBoxDetectionSample,
    image_bounding_box_detection_torchvision_collate_fn,
)


def test_image_bounding_box_detection_torchvision_collate_fn():
    labels_data_0 = create_random_labels_data(n_labels=6, n_classes=3)
    image_data_0 = create_black_image_data(width=128, height=128, n_channels=3)
    bboxes_data_0 = create_random_yolo_bboxes_data(n_bboxes=len(labels_data_0))
    sample_0 = ImageBoundingBoxDetectionSample.create(
        image_data=image_data_0, bboxes_data=bboxes_data_0, labels_data=labels_data_0, bboxes_format="YOLO"
    )

    labels_data_1 = create_random_labels_data(n_labels=3, n_classes=3)
    image_data_1 = create_black_image_data(width=128, height=128, n_channels=3)
    bboxes_data_1 = create_random_yolo_bboxes_data(n_bboxes=len(labels_data_1))
    sample_1 = ImageBoundingBoxDetectionSample.create(
        image_data=image_data_1, bboxes_data=bboxes_data_1, labels_data=labels_data_1, bboxes_format="YOLO"
    )

    dataset = ImageBoundingBoxDetectionDatasetV2(samples=[sample_0, sample_1])
    dataset_sample_0, dataset_sample_1 = dataset[0], dataset[1]

    batch = image_bounding_box_detection_torchvision_collate_fn([dataset_sample_0, dataset_sample_1])

    torch.all(batch["images"][0] == torch.from_numpy(image_data_0).float())
    torch.all(batch["targets"][0]["boxes"] == torch.from_numpy(bboxes_data_0).float())
    torch.all(batch["targets"][0]["labels"] == torch.from_numpy(labels_data_0).type(torch.int64))

    torch.all(batch["images"][1] == torch.from_numpy(image_data_1).float())
    torch.all(batch["targets"][1]["boxes"] == torch.from_numpy(bboxes_data_1).float())
    torch.all(batch["targets"][1]["labels"] == torch.from_numpy(labels_data_1).type(torch.int64))
