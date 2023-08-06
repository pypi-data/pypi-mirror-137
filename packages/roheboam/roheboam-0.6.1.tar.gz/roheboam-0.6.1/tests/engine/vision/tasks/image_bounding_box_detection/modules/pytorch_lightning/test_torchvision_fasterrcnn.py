import numpy as np
import pytest
import torch

from roheboam.engine.testing.image_bounding_box_detection import (
    create_black_image_data,
    create_random_labels_data,
    create_random_pascal_bboxes_data,
)
from roheboam.engine.vision.core.models.torchvision import fasterrcnn_resnet50_fpn


def test_fasterrcnn_resnet50_fpn_prediction_from_batch():
    batch = {
        "images": [
            torch.from_numpy(create_black_image_data(width=128, height=128, n_channels=3, torch_format=False, type=np.float32)) for _ in range(4)
        ],
        "targets": [
            {
                "boxes": torch.from_numpy(create_random_pascal_bboxes_data(max_width=128, max_height=128, n_bboxes=5)),
                "labels": torch.from_numpy(create_random_labels_data(n_labels=5, n_classes=3)),
            }
            for _ in range(4)
        ],
    }
    model = fasterrcnn_resnet50_fpn(num_classes=3)
    model.eval()

    prediction = model(batch["images"])

    assert len(prediction) == 4

    assert "boxes" in prediction[0].keys()
    assert prediction[0]["boxes"].shape == torch.Size([len(prediction[0]["boxes"]), 4])  # shape of N x 4

    assert "labels" in prediction[0].keys()
    assert prediction[0]["labels"].shape == torch.Size([len(prediction[0]["labels"])])  # shape of N

    assert "scores" in prediction[0].keys()
    assert prediction[0]["scores"].shape == torch.Size([len(prediction[0]["scores"])])  # shape of N
