import numpy as np
from miniutils import parallel_progbar

from ..data.sample import create_image_bboxes_detection_sample


def load_label_from_path_ultralytics_format(path):
    labels = np.loadtxt(path).reshape(-1, 5)

    if len(labels) == 0:
        return np.array([])

    return np.array(labels[:, 0].astype(np.int32))


def load_bboxes_from_path_ultralytics_format(path):
    bboxes = np.loadtxt(path).reshape(-1, 5)

    if len(bboxes) == 0:
        return np.array([])

    return np.array(bboxes[:, 1:])


def create_bboxes_detection_samples_data_from_ultralytics_format(
    image_paths, labels_paths, bboxes_format, transform_to_bboxes_format=None, labels_to_keep=None, transform_label_map=None
):
    return np.array(
        [
            {
                "image_path": image_path,
                "labels_path": labels_path,
                "load_labels_fn": load_label_from_path_ultralytics_format,
                "bboxes_path": labels_path,
                "load_bboxes_fn": load_bboxes_from_path_ultralytics_format,
                "bboxes_format": bboxes_format,
                "transform_to_bboxes_format": transform_to_bboxes_format,
                "labels_to_keep": labels_to_keep,
                "transform_label_map": transform_label_map,
            }
            for image_path, labels_path in zip(image_paths, labels_paths)
        ]
    )


def create_bboxes_detection_samples_from_ultralytics_format(
    image_paths, labels_paths, bboxes_format, transform_to_bboxes_format, labels_to_keep=None, transform_label_map=None, first_n_paths=None
):
    assert len(image_paths) == len(labels_paths)
    if first_n_paths is None:
        first_n_paths = len(image_paths)

    samples = parallel_progbar(
        _create_image_bboxes_detection_sample_lambda,
        create_bboxes_detection_samples_data_from_ultralytics_format(
            image_paths[:first_n_paths],
            labels_paths[:first_n_paths],
            bboxes_format,
            transform_to_bboxes_format,
            labels_to_keep,
            transform_label_map,
        ),
    )
    return np.array(samples)


def _create_image_bboxes_detection_sample_lambda(sample_data):
    return create_image_bboxes_detection_sample(**sample_data)


lookup = {
    "load_bbox_from_path_ultralytics_format": load_bboxes_from_path_ultralytics_format,
    "load_label_from_path_ultralytics_format": load_label_from_path_ultralytics_format,
    "create_bboxes_detection_samples_from_ultralytics_format": create_bboxes_detection_samples_from_ultralytics_format,
    "create_bboxes_detection_samples_data_from_ultralytics_format": create_bboxes_detection_samples_data_from_ultralytics_format,
}
