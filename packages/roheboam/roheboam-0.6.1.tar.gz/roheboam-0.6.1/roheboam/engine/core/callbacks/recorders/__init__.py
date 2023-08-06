from .callback_method_is_called_recorder import *
from .image_bounding_box_detection_recorder import *
from .image_classification_recorder import *
from .image_segmentation_recorder import *
from .loss_recorder import *
from .tensorboard_recorder import *

lookup = {
    "CallbackMethodIsCalled": CallbackMethodIsCalledRecorder,
    "CallbackMethodIsCalledRecorder": CallbackMethodIsCalledRecorder,
    "ImageBoundingBoxDetectionResultRecorder": ImageBoundingBoxDetectionResultRecorder,
    "ImageBoundingBoxDetectionInferenceRecorder": ImageBoundingBoxDetectionInferenceRecorder,
    "ImageClassificationResultRecorder": ImageClassificationResultRecorder,
    "ImageClassificationInferenceRecorder": ImageClassificationInferenceRecorder,
    "ImageSegmentationResultRecorder": ImageSegmentationResultRecorder,
    "ImageSegmentationInferenceRecorder": ImageSegmentationInferenceRecorder,
    "PerSampleLossRecorder": PerSampleLossRecorder,
    "TensorboardRecorder": TensorboardRecorder,
}
