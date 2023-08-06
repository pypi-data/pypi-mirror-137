from pathlib import Path
from uuid import uuid4

import matplotlib.pyplot as plt
import numpy as np

from .....core.data import Data
from .....vision.utils.image import imread_rgb


class ImageClassificationSample:
    def __init__(self, image, label=None, name=None):
        self.image = image
        self.label = label
        self.name = str(uuid4()) if name is None else name

    @classmethod
    def create(cls, image_data=None, image_path=None, load_image_fn=imread_rgb, label_data=None, label_path=None, load_label_fn=np.load, name=None):
        if name is None:
            name = Path(image_path).stem if image_path is not None else str(uuid4())

        image = Data(image_data, image_path, load_image_fn)
        if label_data is None and label_path is None:
            label = None
        else:
            label = Data(label_data, label_path, load_label_fn, should_cache=True)
        return cls(image, label, name)

    @property
    def has_label(self):
        return self.label is not None

    @property
    def data(self):
        if self.has_label:
            return self.image.data, self.label.data
        else:
            return self.image.data, None

    def plot(self, figsize=(8, 6)):
        plt.figure(figsize=figsize)
        plt.imshow(self.image.data)
        if self.has_label:
            plt.title(f"Class is: {self.label.data}")

    def create_plot_array(self):
        return self.image.data


def create_image_classification_sample(
    image_data=None, image_path=None, load_image_fn=imread_rgb, label_data=None, label_path=None, load_label_fn=np.load, name=None
):
    return ImageClassificationSample.create(
        image_data=image_data,
        image_path=image_path,
        load_image_fn=load_image_fn,
        label_data=label_data,
        label_path=label_path,
        load_label_fn=load_label_fn,
        name=name,
    )


lookup = {"ImageClassificationSample": ImageClassificationSample, "create_image_classification_sample": create_image_classification_sample}
