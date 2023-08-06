import numpy as np
import torch

from roheboam.engine.core.callbacks import CallbackHandlerContext, Phase, TensorboardRecorder
from roheboam.engine.core.metrics import MeanAveragePrecision, MetricWrapper


def test_tensorboard_recorder_on_validation_epoch_end_for_map_metric(tmp_path):
    # Construct a batch
    targets = [{"boxes": torch.from_numpy(np.ones((1, 4))), "labels": torch.from_numpy(np.array([1])) * i} for i in range(2)]
    predictions = [
        {"boxes": torch.from_numpy(np.ones((1, 4))), "labels": torch.from_numpy(np.array([1])) * i, "scores": torch.from_numpy(np.array([0.5]))}
        for i in range(2)
    ]

    # Setup the context
    context = CallbackHandlerContext()

    mean_average_precision = MeanAveragePrecision(n_classes=3, nms_threshold=0.5, iou_threshold=0.5)
    metric = MetricWrapper(metrics=[mean_average_precision])
    metric(predictions, targets)
    context.validation_metric = metric

    context.current_phase = Phase.VALIDATION
    context.current_epoch = 0
    context.current_step = 0

    # Setup the recorder
    recorder = TensorboardRecorder(root_save_path=tmp_path)
    recorder.validation_step_offset = 0

    # Test
    recorder.on_validation_epoch_end(context)
