from .core import BaseLoss, LossWrapper
from .focal_loss import CrossEntropyLoss, FocalLoss, focal_loss
from .mock_loss import MockSingleLoss
from .torchvision_fasterrcnn_loss import TorchVisionFasterRCNNLoss
from .yolo_loss import YOLOv4Loss, yolo_v4_loss

lookup = {
    "BaseLoss": BaseLoss,
    "LossWrapper": LossWrapper,
    "FocalLoss": FocalLoss,
    "CrossEntropyLoss": CrossEntropyLoss,
    "TorchVisionFasterRCNNLoss": TorchVisionFasterRCNNLoss,
    "MockSingleLoss": MockSingleLoss,
    "YOLOv4Loss": YOLOv4Loss,
    "yolo_v4_loss": yolo_v4_loss,
    "focal_loss": focal_loss,
}
