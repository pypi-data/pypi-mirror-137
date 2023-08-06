from pathlib import Path

import numpy as np

from .....vision.utils.image import imread_rgb


def create_image_classification_samples_data_for_label_per_folder(root_label_folder, label_map, load_image_fn=imread_rgb):
    arguments = []
    for label_folder in Path(root_label_folder).glob("*"):
        for image_path in Path(label_folder).glob("*"):
            arguments.append({"image_path": image_path, "load_image_fn": load_image_fn, "label_data": label_map[label_folder.name]})

    return np.array(arguments)


def create_labels_from_sample_arguments_for_label_per_folder(sample_arguments):
    return sample_arguments, [s["label_data"] for s in sample_arguments]


lookup = {
    "create_image_classification_samples_data_for_label_per_folder": create_image_classification_samples_data_for_label_per_folder,
    "create_labels_from_sample_arguments_for_label_per_folder": create_labels_from_sample_arguments_for_label_per_folder,
}
