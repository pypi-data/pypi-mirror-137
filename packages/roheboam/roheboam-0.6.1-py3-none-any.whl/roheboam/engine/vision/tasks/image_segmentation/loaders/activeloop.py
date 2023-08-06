import hub
import numpy as np
from hub.schema import Image, Segmentation, Text

from .....integrations.activeloop import ActiveLoopHub, compute_activeloop_element
from ..data import create_segmentation_sample


class ImageSegmentationActiveLoopHub(ActiveLoopHub):
    def __init__(self, activeloop_dataset):
        super().__init__(activeloop_dataset)

    @staticmethod
    def create_schema_for_rgb(id_max_shape, image_max_shape, mask_max_shape, label_names):
        return {
            "id": Text(shape=(None,), max_shape=id_max_shape),
            "image": Image(shape=(None, None, 3), dtype="uint8", max_shape=image_max_shape),
            "mask": Segmentation(shape=(None, None), dtype="uint8", names=label_names, max_shape=mask_max_shape),
        }

    @classmethod
    def create_from_url_and_checkout(cls, url, address):
        activeloop_dataset = hub.Dataset(url)
        activeloop_dataset.checkout(address)
        ds = cls(activeloop_dataset)
        return ds

    def create_samples(self):
        return [create_segmentation_sample(**sample_data) for sample_data in self.create_samples_data()]

    def create_samples_data(self):
        arguments = [
            {
                "name": data["id"].compute(),
                "image_path": data["image"],
                "load_image_fn": compute_activeloop_element,
                "mask_path": data["mask"],
                "load_mask_fn": compute_activeloop_element,
            }
            for data in self.activeloop_dataset
        ]
        return np.array(arguments)

    def create_sample_data_from_index(self, index):
        data = self.activeloop_dataset[index]
        return {
            "name": data["id"].compute(),
            "image_path": data["image"],
            "load_image_fn": compute_activeloop_element,
            "mask_path": data["mask"],
            "load_mask_fn": compute_activeloop_element,
        }

    def create_sample_from_index(self, index):
        return create_segmentation_sample(**self.create_sample_data_from_index(index))

    def update_index_with_sample(self, index, sample):
        self.activeloop_dataset["id"][index] = sample.name
        self.activeloop_dataset["image"][index] = sample.image.data
        self.activeloop_dataset["mask"][index] = sample.mask.data


def create_image_segmentation_activeloop_data_from_sample(sample):
    return {"id": sample.name, "image": sample.image.data, "mask": sample.mask.data}


def create_image_segmentation_activeloop_and_checkout(url, address):
    return ImageSegmentationActiveLoopHub.create_from_url_and_checkout(url, address)


lookup = {
    "ImageSegmentationActiveLoopHub": ImageSegmentationActiveLoopHub,
    "create_image_segmentation_activeloop_data_from_sample": create_image_segmentation_activeloop_data_from_sample,
    "create_image_segmentation_activeloop_and_checkout": create_image_segmentation_activeloop_and_checkout,
}
