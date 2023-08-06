import numpy as np
import torch

from roheboam.engine.core.callbacks import CallbackHandlerContext, ImageBoundingBoxDetectionResultRecorder, Phase
from roheboam.engine.utils.convenience import to_numpy


def test_image_bounding_box_detection_recorder_on_validation_batch_end():
    # Construct a batch
    images = [torch.from_numpy(np.ones((3, 512, 512))) * i for i in range(4)]
    targets = [{"boxes": torch.from_numpy(np.ones((1, 4))), "labels": torch.from_numpy(np.array([1])) * i} for i in range(2)]
    predictions = [
        {"boxes": torch.from_numpy(np.ones((1, 4))), "labels": torch.from_numpy(np.array([1])) * i, "scores": torch.from_numpy(np.array([0.5]))}
        for i in range(2)
    ]
    batch = {"images": images, "targets": targets}

    # Setup the context
    context = CallbackHandlerContext()
    context.current_phase = Phase.VALIDATION
    context.current_epoch = 0
    context.current_step = 0
    context.validation_batch = batch
    context.validation_prediction = predictions

    # Setup the recorder
    recorder = ImageBoundingBoxDetectionResultRecorder(convert_tensor_to_labels_fn=to_numpy, convert_tensor_to_scores_fn=to_numpy)

    # Test
    recorder.on_validation_batch_end(context)

    # Assert
    sample_0 = recorder.results[str(Phase.VALIDATION), 0][0]
    sample_1 = recorder.results[str(Phase.VALIDATION), 0][1]
    assert torch.all(sample_0["image"] == torch.from_numpy(np.ones((3, 512, 512)) * 0))
    assert torch.all(sample_0["predicted_boxes"] == torch.from_numpy(np.ones((1, 4))))
    assert np.all(sample_0["predicted_labels"] == np.array([1]) * 0)
    assert np.all(sample_0["predicted_scores"] == np.array([0.5]))
    assert torch.all(sample_0["truth_boxes"] == torch.from_numpy(np.ones((1, 4))))
    assert np.all(sample_0["truth_labels"] == np.array([1]) * 0)

    assert torch.all(sample_1["image"] == torch.from_numpy(np.ones((3, 512, 512)) * 1))
    assert torch.all(sample_1["predicted_boxes"] == torch.from_numpy(np.ones((1, 4))))
    assert np.all(sample_1["predicted_labels"] == np.array([1]) * 1)
    assert np.all(sample_1["predicted_scores"] == np.array([0.5]))
    assert torch.all(sample_1["truth_boxes"] == torch.from_numpy(np.ones((1, 4))))
    assert np.all(sample_1["truth_labels"] == np.array([1]) * 1)


def test_create_samples_with_thresholds_from_result():
    result = {
        "image": np.zeros((480, 640, 3)),
        "predicted_boxes": np.array(
            [
                [3.0938702e02, 1.7543335e-01, 6.4000000e02, 2.8213779e02],
                [0.0000000e00, 5.6033680e01, 6.4000000e02, 3.6025177e02],
                [3.2138623e02, 0.0000000e00, 6.4000000e02, 3.9072781e02],
                [3.1091698e01, 1.1477293e02, 3.8777362e02, 4.8000003e02],
                [5.9970448e01, 1.0265663e02, 5.0962375e02, 3.1092572e02],
                [2.6265756e02, 0.0000000e00, 6.0189868e02, 2.3590427e02],
                [1.6797735e01, 9.6240425e01, 4.7715622e02, 4.3279111e02],
                [3.0023251e00, 6.4484238e01, 2.2136465e02, 4.8000003e02],
            ]
        ),
        "predicted_scores": np.array([0.21236542, 0.08359145, 0.08068511, 0.06804989, 0.0650317, 0.05558778, 0.05447339, 0.05183122]),
        "predicted_labels": np.array([16, 16, 25, 16, 16, 23, 23, 16]),
        "truth_boxes": np.array(
            [
                [1.0800000e00, 1.8769008e02, 6.1266974e02, 4.7353009e02],
                [3.1173026e02, 4.3101602e00, 6.3101025e02, 2.3299033e02],
                [2.4960033e02, 2.2927032e02, 5.6584033e02, 4.7435016e02],
                [3.1999999e-04, 1.3510080e01, 4.3448032e02, 3.8863007e02],
                [3.7620001e02, 4.0360081e01, 4.5175009e02, 8.6889839e01],
                [4.6577985e02, 3.8970001e01, 5.2384961e02, 8.5639923e01],
                [3.8570016e02, 7.3659843e01, 4.6972000e02, 1.4416992e02],
                [3.6404959e02, 2.4902401e00, 4.5880991e02, 7.3559998e01],
            ]
        ),
        "truth_labels": np.array([45, 45, 50, 45, 49, 49, 49, 49]),
    }

    recorder = ImageBoundingBoxDetectionResultRecorder()
    thresholds = np.arange(0, 1, 0.2)
    samples_with_thresholds = recorder.create_samples_with_thresholds_from_result(
        result, bboxes_format="PASCAL_VOC", thresholds=thresholds, include_truth=True
    )

    assert len(samples_with_thresholds) == len(thresholds) + 1  # for truth
    assert list(samples_with_thresholds.keys()) == ["0.0", "0.2", "0.4", "0.6", "0.8", "truth"]
