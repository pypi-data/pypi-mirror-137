from collections import defaultdict

from ....utils.convenience import to_numpy
from ..callback import Callback
from .utils import ShouldRecordMixin


class ImageSegmentationResultRecorder(Callback, ShouldRecordMixin):

    _order = -10

    def __init__(
        self,
        train_merge_tiles_fn=lambda x: x,
        inference_merge_tiles_fn=lambda x: x,
        convert_tensor_to_image_fn=lambda x: x,
        convert_tensor_to_mask_fn=lambda x: x,
        record_on_validation=True,
        record_on_test=True,
        record_every_n_steps=25,
        name=None,
    ):
        super().__init__(name)
        self.train_merge_tiles_fn = train_merge_tiles_fn
        self.inference_merge_tiles_fn = inference_merge_tiles_fn
        self.convert_tensor_to_image_fn = convert_tensor_to_image_fn
        self.convert_tensor_to_mask_fn = convert_tensor_to_mask_fn
        self.record_on_validation = record_on_validation
        self.record_on_test = record_on_test
        self.record_every_n_steps = record_every_n_steps
        self.results = defaultdict(list)

    def on_train_batch_end(self, context):

        phase, epoch, step, batch, predictions = (
            context.current_phase,
            context.current_epoch,
            context.current_step,
            context.train_batch,
            context.train_prediction,
        )

        if not self._should_store(phase, epoch, step):
            return

        images = self.train_merge_tiles_fn(self.convert_tensor_to_image_fn(batch["images"]))
        raw_predictions = self.train_merge_tiles_fn(to_numpy(predictions).transpose(0, 2, 3, 1))
        final_predictions = self.train_merge_tiles_fn(self.convert_tensor_to_mask_fn(predictions))
        masks = self.train_merge_tiles_fn(self.convert_tensor_to_mask_fn(batch["masks"]))
        self.results[(str(phase), epoch)].extend(
            [
                {"image": image, "prediction": raw_prediction, "final_prediction": final_prediction, "mask": mask}
                for image, raw_prediction, final_prediction, mask in zip(images, raw_predictions, final_predictions, masks)
            ]
        )

    def on_validation_batch_end(self, context):
        phase, epoch, step, batch, predictions = (
            context.current_phase,
            context.current_epoch,
            context.current_step,
            context.validation_batch,
            context.validation_prediction,
        )
        if not self._should_store(phase, epoch, step):
            return

        images = self.inference_merge_tiles_fn(self.convert_tensor_to_image_fn(batch["images"]))
        raw_predictions = self.inference_merge_tiles_fn(to_numpy(predictions).transpose(0, 2, 3, 1))
        final_predictions = self.inference_merge_tiles_fn(self.convert_tensor_to_mask_fn(predictions))
        masks = self.inference_merge_tiles_fn(self.convert_tensor_to_mask_fn(batch["masks"]))
        self.results[str(phase), epoch].extend(
            [
                {"image": image, "prediction": raw_prediction, "final_prediction": final_prediction, "mask": mask}
                for image, raw_prediction, final_prediction, mask in zip(images, raw_predictions, final_predictions, masks)
            ]
        )

    def on_test_batch_end(self, context):
        phase, epoch, step, batch, predictions = (
            context.current_phase,
            context.current_epoch,
            context.current_step,
            context.test_batch,
            context.test_prediction,
        )
        if not self._should_store(phase, epoch, step):
            return

        images = self.inference_merge_tiles_fn(self.convert_tensor_to_image_fn(batch["images"]))
        raw_predictions = self.inference_merge_tiles_fn(to_numpy(predictions).transpose(0, 2, 3, 1))
        final_predictions = self.inference_merge_tiles_fn(self.convert_tensor_to_mask_fn(predictions))
        has_masks = "masks" in batch

        if has_masks:
            masks = self.inference_merge_tiles_fn(self.convert_tensor_to_mask_fn(batch["masks"]))
            result = [
                {"image": image, "prediction": raw_prediction, "final_prediction": final_prediction, "mask": mask}
                for image, raw_prediction, final_prediction, mask in zip(images, raw_predictions, final_predictions, masks)
            ]
        else:
            result = [
                {"image": image, "prediction": raw_prediction, "final_prediction": final_prediction}
                for image, raw_prediction, final_prediction, in zip(images, raw_predictions, final_predictions)
            ]
        self.results[(str(phase), epoch)].extend(result)


class ImageSegmentationInferenceRecorder(Callback):

    _order = -10

    def __init__(
        self, inference_merge_tiles_fn=lambda x: x, convert_tensor_to_image_fn=lambda x: x, convert_tensor_to_mask_fn=lambda x: x, name=None
    ):
        super().__init__(name)
        self.inference_merge_tiles_fn = inference_merge_tiles_fn
        self.convert_tensor_to_image_fn = convert_tensor_to_image_fn
        self.convert_tensor_to_mask_fn = convert_tensor_to_mask_fn
        self.results = []

    @property
    def output(self):
        return dict(
            names=self.names,
            input=self.inputs,
            predicted_prob_for_masks=self.predicted_prob_for_masks,
            predicted_masks=self.predicted_masks,
            true_masks=self.true_masks,
        )

    def flush_results(self):
        self.results = []

    def on_test_batch_end(self, context):
        _, _, batch, predictions = (context.current_phase, context.current_epoch, context.test_batch, context.test_prediction)
        images = self.convert_tensor_to_image_fn(batch["images"])
        raw_predictions = self.inference_merge_tiles_fn(to_numpy(predictions))
        final_predictions = self.inference_merge_tiles_fn(self.convert_tensor_to_mask_fn(predictions))
        self.results.extend(
            [
                {"image": image, "prediction": raw_prediction, "final_prediction": final_prediction}
                for image, raw_prediction, final_prediction in zip(images, raw_predictions, final_predictions)
            ]
        )
