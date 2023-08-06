from collections import defaultdict

from ....utils.convenience import to_numpy
from ..callback import Callback


class ImageClassificationResultRecorder(Callback):

    _order = -10

    def __init__(self, convert_tensor_to_image_fn=None, name=None):
        super().__init__(name)
        self.convert_tensor_to_image_fn = convert_tensor_to_image_fn
        self.results = defaultdict(list)

    def on_train_batch_end(self, context):
        phase, epoch, batch, predictions = (context.current_phase, context.current_epoch, context.train_batch, context.train_prediction)
        images = self.convert_tensor_to_image_fn(batch["images"])
        predictions = to_numpy(predictions)
        labels = to_numpy(batch["labels"])
        self.results[str(phase), epoch].extend(
            [{"image": image, "prediction": prediction, "label": label} for image, prediction, label in zip(images, predictions, labels)]
        )

    def on_validation_batch_end(self, context):
        phase, epoch, batch, predictions = (context.current_phase, context.current_epoch, context.validation_batch, context.validation_prediction)
        images = self.convert_tensor_to_image_fn(batch["images"])
        predictions = to_numpy(predictions)
        labels = to_numpy(batch["labels"])
        self.results[str(phase), epoch].extend(
            [{"image": image, "prediction": prediction, "label": label} for image, prediction, label in zip(images, predictions, labels)]
        )

    def on_test_batch_end(self, context):
        phase, epoch, batch, predictions = (context.current_phase, context.current_epoch, context.test_batch, context.test_prediction)
        images = self.convert_tensor_to_image_fn(batch["images"])
        predictions = to_numpy(predictions)
        labels_exists = "labels" in batch

        if labels_exists:
            labels = to_numpy(batch["labels"])
            results = [{"image": image, "prediction": prediction, "label": label} for image, prediction, label in zip(images, predictions, labels)]
        else:
            results = [{"image": image, "prediction": prediction} for image, prediction in zip(images, predictions)]

        self.results[str(phase), epoch].extend(results)


class ImageClassificationInferenceRecorder(Callback):

    _order = -10

    def __init__(self, convert_tensor_to_image_fn=None, name=None):
        super().__init__(name)
        self.convert_tensor_to_image_fn = convert_tensor_to_image_fn
        self.results = []

    def flush_results(self):
        self.results = []

    def on_test_batch_end(self, context):
        _, _, batch, predictions = (context.current_phase, context.current_epoch, context.test_batch, context.test_prediction)
        images = self.convert_tensor_to_image_fn(batch["images"])
        predictions = to_numpy(predictions)
        self.results.extend([{"image": image, "prediction": prediction} for image, prediction in zip(images, predictions)])
