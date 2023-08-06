import mlflow
from pytorch_lightning.utilities.cloud_io import load as pl_load

from roheboam.engine import get_toolbox_lookup


class MLFlowPyfuncImageBoundingBoxDetectionModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.lookup = get_toolbox_lookup()
        self.config = self.lookup["load_config_from_path"](context.artifacts["config_path"])
        self.config["Variables"]["is_deployed"] = True
        self.pipeline = self.lookup["Pipeline"].create_from_config(self.config, self.lookup)
        self.pipeline.run(remove_nodes_with_tags=["TRAIN"])
        self.module = self.pipeline.get_node_output("ModuleCreator")()
        self.trainer = self.pipeline.get_node_output("TrainerCreator")()
        self.inference_recorder = self.pipeline.get_node_output("ImageBoundingBoxDetectionInferenceRecorder")

        pl_checkpoint = pl_load(context.artifacts["model_save_path"], map_location=lambda storage, loc: storage)
        self.module.load_state_dict(pl_checkpoint["state_dict"])

    def preload_context(self, context):
        pass

    def predict(self, context, model_input):
        if "images" in model_input:
            samples_data = [{"image_data": self.lookup["to_uint8_image"](image)} for image in model_input["images"]]
        if "image_paths" in model_input:
            samples_data = [
                {"image_path": image_path, "load_image_fn": lambda p: self.lookup["to_uint8_image"](self.lookup["imread_rgb"](p))}
                for image_path in model_input["image_paths"]
            ]

        samples = [self.lookup["create_image_bboxes_detection_sample"](**sample_data) for sample_data in samples_data]

        test_dataset = self.pipeline.get_node_output("TestDatasetCreator")(samples=samples)
        test_dataloader = self.pipeline.get_node_output("TestDataLoaderCreator")(test_dataset)
        results = self.inference_recorder.create_results_from_dataloader(test_dataloader, self.trainer, self.module)
        samples_with_thresholds = [
            self.inference_recorder.create_samples_with_thresholds_from_result(result, bboxes_format="PASCAL_VOC") for result in results
        ]
        bbox_predictions_for_thresholds_for_samples = {}

        for sample_with_thresholds in samples_with_thresholds:
            sample_name = [s for s in sample_with_thresholds.values()][0].name
            bbox_predictions_for_thresholds_for_samples[sample_name] = {}
            for threshold, sample in sample_with_thresholds.items():
                bbox_predictions_for_thresholds_for_samples[sample_name][threshold] = {
                    "labels": sample.labels.data.tolist(),
                    "bboxes": sample.bboxes.data.tolist(),
                }

        return bbox_predictions_for_thresholds_for_samples


lookup = {"MLFlowPyfuncImageBoundingBoxDetectionModel": MLFlowPyfuncImageBoundingBoxDetectionModel}
