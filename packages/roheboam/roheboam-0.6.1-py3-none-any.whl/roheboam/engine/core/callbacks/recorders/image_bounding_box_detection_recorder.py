from collections import defaultdict
from copy import deepcopy

import numpy as np

from ....utils.convenience import to_numpy
from ....vision.utils.bbox import nms_with_scores
from ....vision.utils.image import plot_image_grid
from ..callback import Callback
from .utils import ShouldRecordMixin


class _PlotMixins:
    def plot_sample_with_thresholds(self, sample_with_thresholds, ncols=None, figsize=None):
        images, titles = self.create_images_and_titles_from_sample_with_thresholds(sample_with_thresholds)
        plot_image_grid(images, titles=titles, ncols=ncols, figsize=figsize)

    def create_images_and_titles_from_sample_with_thresholds(self, sample_with_thresholds):
        images = []
        titles = []
        for threshold, sample in sample_with_thresholds.items():
            images.append(sample.create_plot_array())
            titles.append(threshold)
        return images, titles


class _InferenceMixins:
    def create_samples_with_thresholds_from_samples_with_pipeline(self, samples, pipeline, trainer, module, thresholds=np.arange(0, 1, 0.2)):
        dataloader = pipeline.get_node_output("TestDataLoaderCreator")(pipeline.get_node_output("TestDatasetCreator")(samples))
        results = self.create_results_from_dataloader(dataloader, trainer, module)
        return [
            self.create_samples_with_thresholds_from_result(result, sample.bboxes_format, thresholds) for sample, result in zip(samples, results)
        ]

    def create_samples_with_thresholds_from_samples_data_with_pipeline(
        self, samples_data, pipeline, trainer, module, thresholds=np.arange(0, 1, 0.2)
    ):
        dataloader = pipeline.get_node_output("TestDataLoaderCreator")(pipeline.get_node_output("TestDatasetCreator")(samples_data))
        results = self.create_results_from_dataloader(dataloader, trainer, module)
        return [self.create_samples_with_thresholds_from_result(result, thresholds) for result in results]

    def create_results_from_dataloader(self, dataloader, trainer, module):
        trainer.test(module, test_dataloaders=[dataloader])
        results = deepcopy(self.results)
        self.flush_results()
        return results

    def create_samples_with_thresholds_from_result(self, result, bboxes_format, thresholds=np.arange(0, 1, 0.2), include_truth=True):
        sample_with_thresholds = {
            str(np.around(threshold, 2)): self.create_predicted_sample(result, bboxes_format, threshold) for threshold in thresholds
        }

        if include_truth and "truth_labels" in result and "truth_boxes" in result:
            sample_with_thresholds["truth"] = self.create_truth_sample(result, bboxes_format)
        return sample_with_thresholds

    def create_predicted_and_truth_samples(self, result, bboxes_format, iou_threshold=0.2):
        predicted_sample = self.create_predicted_sample(result, bboxes_format, iou_threshold)
        truth_sample = self.create_truth_sample(result, bboxes_format)
        return predicted_sample, truth_sample

    def create_predicted_sample(self, result, bboxes_format, iou_threshold=0.2):
        from ....vision.tasks.image_bounding_box_detection.data import ImageBoundingBoxDetectionSample

        nms_outputs = nms_with_scores(
            result["predicted_boxes"], result["predicted_scores"], result["predicted_labels"], iou_threshold=iou_threshold
        )
        predicted_sample = ImageBoundingBoxDetectionSample.create(
            image_data=result["image"], labels_data=nms_outputs["labels"], bboxes_data=nms_outputs["boxes"], bboxes_format=bboxes_format
        )
        return predicted_sample

    def create_truth_sample(self, result, bboxes_format):
        from ....vision.tasks.image_bounding_box_detection.data import ImageBoundingBoxDetectionSample

        truth_sample = ImageBoundingBoxDetectionSample.create(
            image_data=result["image"], labels_data=result["truth_labels"], bboxes_data=result["truth_boxes"], bboxes_format=bboxes_format
        )
        return truth_sample


class ImageBoundingBoxDetectionResultRecorder(Callback, ShouldRecordMixin, _InferenceMixins, _PlotMixins):

    _order = -10

    def __init__(
        self,
        convert_tensor_to_image_fn=lambda x: x,
        convert_tensor_to_bboxes_fn=lambda x: x,
        convert_tensor_to_labels_fn=to_numpy,
        convert_tensor_to_scores_fn=to_numpy,
        record_on_validation=True,
        record_on_test=True,
        record_every_n_steps=25,
        name=None,
    ):
        super().__init__(name)
        self.convert_tensor_to_image_fn = convert_tensor_to_image_fn
        self.convert_tensor_to_bboxes_fn = convert_tensor_to_bboxes_fn
        self.convert_tensor_to_labels_fn = convert_tensor_to_labels_fn
        self.convert_tensor_to_scores_fn = convert_tensor_to_scores_fn
        self.record_on_validation = record_on_validation
        self.record_on_test = record_on_test
        self.record_every_n_steps = record_every_n_steps
        self.results = defaultdict(list)

    def on_train_batch_end(self, context):

        phase, epoch, step, batch, _ = (
            context.current_phase,
            context.current_epoch,
            context.current_step,
            context.train_batch,
            context.train_prediction,
        )

        if not self._should_store(phase, epoch, step):
            return

        self.results[(str(phase), epoch)].extend([{"image": self.convert_tensor_to_image_fn(image)} for image in batch["images"]])

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

        self.results[(str(phase), epoch)].extend(
            [
                {
                    "image": self.convert_tensor_to_image_fn(image),
                    "predicted_boxes": self.convert_tensor_to_bboxes_fn(prediction["boxes"]),
                    "predicted_scores": self.convert_tensor_to_scores_fn(prediction["scores"]),
                    "predicted_labels": self.convert_tensor_to_labels_fn(prediction["labels"]),
                    "truth_boxes": self.convert_tensor_to_bboxes_fn(target["boxes"]),
                    "truth_labels": self.convert_tensor_to_labels_fn(target["labels"]),
                }
                for image, target, prediction in zip(batch["images"], batch["targets"], predictions)
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

        self.results[(str(phase), epoch)].extend(
            [
                {
                    "image": self.convert_tensor_to_image_fn(image),
                    "predicted_boxes": self.convert_tensor_to_bboxes_fn(prediction["boxes"]),
                    "predicted_scores": self.convert_tensor_to_scores_fn(prediction["scores"]),
                    "predicted_labels": self.convert_tensor_to_labels_fn(prediction["labels"]),
                    "truth_boxes": self.convert_tensor_to_bboxes_fn(target["boxes"]),
                    "truth_labels": self.convert_tensor_to_labels_fn(target["labels"]),
                }
                for image, target, prediction in zip(batch["images"], batch["targets"], predictions)
            ]
        )


class ImageBoundingBoxDetectionInferenceRecorder(Callback, _InferenceMixins, _PlotMixins):
    _order = -10

    def __init__(
        self,
        convert_tensor_to_image_fn=lambda x: x,
        convert_tensor_to_bboxes_fn=lambda x: x,
        convert_tensor_to_labels_fn=to_numpy,
        convert_tensor_to_scores_fn=to_numpy,
        name=None,
    ):
        super().__init__(name)
        self.convert_tensor_to_image_fn = convert_tensor_to_image_fn
        self.convert_tensor_to_bboxes_fn = convert_tensor_to_bboxes_fn
        self.convert_tensor_to_labels_fn = convert_tensor_to_labels_fn
        self.convert_tensor_to_scores_fn = convert_tensor_to_scores_fn
        self.results = []

    def flush_results(self):
        self.results = []

    def on_test_batch_end(self, context):
        batch, predictions = (context.test_batch, context.test_prediction)

        if "targets" in batch:
            self.results.extend(
                [
                    {
                        "image": self.convert_tensor_to_image_fn(image),
                        "predicted_boxes": self.convert_tensor_to_bboxes_fn(prediction["boxes"]),
                        "predicted_scores": self.convert_tensor_to_scores_fn(prediction["scores"]),
                        "predicted_labels": self.convert_tensor_to_labels_fn(prediction["labels"]),
                        "truth_boxes": self.convert_tensor_to_bboxes_fn(target["boxes"]),
                        "truth_labels": self.convert_tensor_to_labels_fn(target["labels"]),
                    }
                    for image, target, prediction in zip(batch["images"], batch["targets"], predictions)
                ]
            )
        else:
            self.results.extend(
                [
                    {
                        "image": self.convert_tensor_to_image_fn(image),
                        "predicted_boxes": self.convert_tensor_to_bboxes_fn(prediction["boxes"]),
                        "predicted_scores": self.convert_tensor_to_scores_fn(prediction["scores"]),
                        "predicted_labels": self.convert_tensor_to_labels_fn(prediction["labels"]),
                    }
                    for image, prediction in zip(batch["images"], predictions)
                ]
            )
