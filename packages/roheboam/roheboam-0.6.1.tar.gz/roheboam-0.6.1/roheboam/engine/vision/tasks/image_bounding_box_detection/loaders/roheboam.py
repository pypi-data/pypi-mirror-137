import json
from glob import glob
from pathlib import Path

import numpy as np
from miniutils import parallel_progbar

from ..data.sample import create_image_bboxes_detection_sample


def roheboam_sample_data_paths_from_path(root_path, category):
    image_paths = []
    label_paths = []
    for sample_directory in Path(root_path).glob("*"):
        metadata_path = sample_directory / "metadata.json"
        if not (metadata_path).exists():
            continue

        metadata = json.load(open(metadata_path))
        sample_category = metadata["category"]
        imagePath = metadata["imagePath"]
        labelPath = metadata["labelPath"]
        assert metadata["labelType"] == "ULTRALYTICS"

        absolute_image_path = metadata_path.parent / imagePath
        absolute_label_path = metadata_path.parent / labelPath if labelPath is not None else None

        if sample_category == category:
            image_paths.append(absolute_image_path)
            label_paths.append(absolute_label_path)

    return image_paths, label_paths


def load_label_from_path_roheboam_format(path):
    labels = np.loadtxt(path).reshape(-1, 5)

    if len(labels) == 0:
        return np.array([])

    return np.array(labels[:, 0].astype(np.int32))


def load_bboxes_from_path_roheboam_format(path):
    bboxes = np.loadtxt(path).reshape(-1, 5)

    if len(bboxes) == 0:
        return np.array([])

    return np.array(bboxes[:, 1:])


def create_bboxes_detection_samples_data_from_roheboam_format(
    image_paths, labels_paths, bboxes_format, transform_to_bboxes_format=None, labels_to_keep=None, transform_label_map=None
):
    return np.array(
        [
            {
                "image_path": image_path,
                "labels_path": labels_path,
                "load_labels_fn": load_label_from_path_roheboam_format,
                "bboxes_path": labels_path,
                "load_bboxes_fn": load_bboxes_from_path_roheboam_format,
                "bboxes_format": bboxes_format,
                "transform_to_bboxes_format": transform_to_bboxes_format,
                "labels_to_keep": labels_to_keep,
                "transform_label_map": transform_label_map,
            }
            for image_path, labels_path in zip(image_paths, labels_paths)
        ]
    )


def create_bboxes_detection_samples_from_roheboam_format(
    image_paths, labels_paths, bboxes_format, transform_to_bboxes_format, labels_to_keep=None, transform_label_map=None, first_n_paths=None
):
    assert len(image_paths) == len(labels_paths)
    if first_n_paths is None:
        first_n_paths = len(image_paths)
    samples = parallel_progbar(
        lambda sample_data: create_image_bboxes_detection_sample(**sample_data),
        create_bboxes_detection_samples_data_from_roheboam_format(
            image_paths[:first_n_paths],
            labels_paths[:first_n_paths],
            bboxes_format,
            transform_to_bboxes_format,
            labels_to_keep,
            transform_label_map,
        ),
    )
    return np.array(samples)


lookup = {
    "roheboam_sample_data_paths_from_path": roheboam_sample_data_paths_from_path,
    "load_bbox_from_path_roheboam_format": load_bboxes_from_path_roheboam_format,
    "load_label_from_path_roheboam_format": load_label_from_path_roheboam_format,
    "create_bboxes_detection_samples_from_roheboam_format": create_bboxes_detection_samples_from_roheboam_format,
    "create_bboxes_detection_samples_data_from_roheboam_format": create_bboxes_detection_samples_data_from_roheboam_format,
}
