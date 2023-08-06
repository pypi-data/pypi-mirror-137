import hub
import numpy as np
from hub.schema import BBox, ClassLabel, Image, Text

from .....integrations.activeloop import ActiveLoopHub, compute_activeloop_element
from ..data import create_image_bboxes_detection_sample


class ImageBoundingBoxDetectionActiveLoopHub(ActiveLoopHub):
    def __init__(self, activeloop_dataset):
        super().__init__(activeloop_dataset)

    @staticmethod
    def create_schema_for_rgb(id_max_shape, image_max_shape, bbox_max_shape, label_names=None, num_classes=None):
        assert (label_names is None) ^ (num_classes is None)
        if label_names:
            class_label_args = {"names": label_names}
        if num_classes:
            class_label_args = {"num_classes": num_classes}

        return {
            "id": Text(shape=(None,), max_shape=id_max_shape),
            "image": Image(shape=(None, None, 3), dtype="uint8", max_shape=image_max_shape),
            "bboxes": BBox(shape=(None, 4), max_shape=bbox_max_shape),
            "labels": ClassLabel(shape=(None,), max_shape=(bbox_max_shape[0],), **class_label_args),
        }

    @classmethod
    def create_from_url(cls, url):
        activeloop_dataset = hub.Dataset(url)
        ds = cls(activeloop_dataset)
        return ds

    @classmethod
    def create_from_url_and_checkout(cls, url, address):
        activeloop_dataset = hub.Dataset(url)
        activeloop_dataset.checkout(address)
        ds = cls(activeloop_dataset)
        return ds

    def create_samples(self):
        return [create_image_bboxes_detection_sample(**sample_data) for sample_data in self.create_samples_data()]

    def create_samples_data(self, bboxes_format="YOLO"):
        arguments = [
            {
                "name": data["id"].compute(),
                "image_path": data["image"],
                "load_image_fn": compute_activeloop_element,
                "bboxes_path": data["bboxes"],
                "load_bboxes_fn": compute_activeloop_element,
                "labels_path": data["labels"],
                "load_labels_fn": compute_activeloop_element,
                "bboxes_format": bboxes_format,
            }
            for data in self.activeloop_dataset
        ]
        return np.array(arguments)

    def create_sample_data_from_index(self, index, bboxes_format="YOLO"):
        data = self.activeloop_dataset[index]
        return {
            "name": data["id"].compute(),
            "image_path": data["image"],
            "load_image_fn": compute_activeloop_element,
            "bboxes_path": data["bboxes"],
            "load_bboxes_fn": compute_activeloop_element,
            "bboxes_format": bboxes_format,
            "labels_path": data["labels"],
            "load_labels_fn": compute_activeloop_element,
        }

    def create_sample_from_index(self, index, bboxes_format="YOLO"):
        return create_image_bboxes_detection_sample(**self.create_sample_data_from_index(index, bboxes_format))

    def update_index_with_sample(self, index, sample):
        self.activeloop_dataset["id"][index] = sample.name
        self.activeloop_dataset["image"][index] = sample.image.data
        self.activeloop_dataset["bboxes"][index] = sample.bboxes.data
        self.activeloop_dataset["labels"][index] = sample.labels.data


def create_image_bounding_box_detection_activeloop_data_from_sample(sample):
    return ({"id": sample.name, "image": sample.image.data, "labels": sample.labels.data, "bboxes": sample.bboxes.data},)


def create_image_bounding_box_detection_activeloop_and_checkout(url, address):
    return ImageBoundingBoxDetectionActiveLoopHub.create_from_url_and_checkout(url, address)


lookup = {
    "ImageBoundingBoxDetectionActiveLoopHub": ImageBoundingBoxDetectionActiveLoopHub,
    "create_image_bounding_box_detection_activeloop_data_from_sample": create_image_bounding_box_detection_activeloop_data_from_sample,
    "create_image_bounding_box_detection_activeloop_and_checkout": create_image_bounding_box_detection_activeloop_and_checkout,
}
