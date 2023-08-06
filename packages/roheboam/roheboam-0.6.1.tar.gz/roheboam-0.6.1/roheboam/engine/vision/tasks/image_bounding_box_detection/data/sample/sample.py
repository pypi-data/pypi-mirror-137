import random
from functools import partial
from pathlib import Path
from uuid import uuid4

import matplotlib.pyplot as plt
import numpy as np

from ......core.data import Data
from ......utils.convenience import class_path_with_default
from ......vision.utils import (
    clip_bboxes,
    cxcywh_to_xyxy,
    denormalize_bboxes_for_image,
    imread_rgb,
    plot_bounding_boxes_on_image_with_label,
    xywh_to_xyxy,
)


class _DataMixin:
    @property
    def data(self):
        return (
            self.image.data,
            self.bboxes.data if self.bboxes_exists else None,
            self.labels.data if self.labels_exists else None,
            self.name if self.name is not None else None,
        )

    # @property
    # def sample_data(self):
    #     return {
    #         "image_data": class_path_with_default(["image", "data"], self),
    #         "image_path": class_path_with_default(["image", "path"], self),
    #         "load_image_fn": class_path_with_default(["image", "load_fn"], self),
    #         "labels_data": class_path_with_default(["labels", "data"], self),
    #         "labels_path": class_path_with_default(["labels", "path"], self),
    #         "load_labels_fn": class_path_with_default(["labels", "load_fn"], self),
    #         "bboxes_data": class_path_with_default(["bboxes", "data"], self),
    #         "bboxes_path": class_path_with_default(["bboxes", "path"], self),
    #         "load_bboxes_fn": class_path_with_default(["bboxes", "load_fn"], self),
    #         "_bboxes_format": self._bboxes_format,
    #         "name": self.name,
    #     }

    # @property
    # def sample_data_without_loaded_data(self):
    #     return {
    #         "image_path": class_path_with_default(["image", "path"], self),
    #         "load_image_fn": class_path_with_default(["image", "load_fn"], self),
    #         "labels_path": class_path_with_default(["labels", "path"], self),
    #         "load_labels_fn": class_path_with_default(["labels", "load_fn"], self),
    #         "bboxes_path": class_path_with_default(["bboxes", "path"], self),
    #         "load_bboxes_fn": class_path_with_default(["bboxes", "load_fn"], self),
    #         "_bboxes_format": self._bboxes_format,
    #         "name": self.name,
    #     }

    @data.setter
    def data(self, image=None, bboxes=None, labels=None):
        if image is not None:
            self.image.data = image
        if bboxes is not None:
            self.bboxes.data = bboxes
        if labels is not None:
            self.labels.data = labels


class _PlotMixin:
    def plot(self, labels_to_plot=None, figsize=(8, 6)):
        if self.bboxes_exists and self.labels_exists:
            if labels_to_plot is not None:
                idxs_to_keep = [i for (i, l) in enumerate(self.labels.data) if l in labels_to_plot]
                plt.figure(figsize=figsize)
                plt.imshow(
                    plot_bounding_boxes_on_image_with_label(self.image.data, self.pascal_voc_bboxes[idxs_to_keep], self.labels.data[idxs_to_keep])
                )
            else:
                plt.figure(figsize=figsize)
                plt.imshow(plot_bounding_boxes_on_image_with_label(self.image.data, self.pascal_voc_bboxes, self.labels.data))
        else:
            plt.imshow(self.image.data)

    def create_plot_array(self, labels_to_plot=None):
        if self.bboxes_exists and self.labels_exists:
            if labels_to_plot is not None:
                idxs_to_keep = [i for (i, l) in enumerate(self.labels.data) if l in labels_to_plot]
                return plot_bounding_boxes_on_image_with_label(
                    self.image.data, self.pascal_voc_bboxes[idxs_to_keep], self.labels.data[idxs_to_keep]
                )
            else:
                return plot_bounding_boxes_on_image_with_label(self.image.data, self.pascal_voc_bboxes, self.labels.data)
        else:
            return self.image.data


class _BoundingBoxMixin:
    @property
    def labels(self):
        self._labels.run_fns_to_run()
        return self._labels

    @property
    def bboxes_format(self):
        self.bboxes
        return self._bboxes_format

    @property
    def bboxes(self):
        if self._convert_to_pascal_voc_bboxes_in_future:
            self.convert_to_pascal_voc_bboxes(lazy=False)
            self._convert_to_pascal_voc_bboxes_in_future = False
            self._bboxes_format = "PASCAL_VOC"
        self._bboxes.run_fns_to_run()
        return self._bboxes

    @property
    def pascal_voc_bboxes(self):
        height, width, _ = self.image.data.shape
        bboxes_format = self.bboxes_format
        bboxes = self.bboxes.data
        return self._create_pascal_voc_bboxes(height, width, bboxes, bboxes_format)

    def convert_to_pascal_voc_bboxes(self, lazy=True):
        if self.bboxes_exists and lazy:
            self._convert_to_pascal_voc_bboxes_in_future = True

        if self.bboxes_exists and not lazy:
            height, width, _ = self.image.data.shape
            self._bboxes.data = self._create_pascal_voc_bboxes(height, width, self._bboxes.data, self._bboxes_format)
            self._bboxes_format = "PASCAL_VOC"

    def _create_pascal_voc_bboxes(self, image_height, image_width, bboxes, bboxes_format):
        if bboxes_format == "PASCAL_VOC":
            return bboxes
        elif bboxes_format == "YOLO":
            bboxes = cxcywh_to_xyxy(denormalize_bboxes_for_image(bboxes, height=image_height, width=image_width))
        elif bboxes_format == "COCO":
            bboxes = xywh_to_xyxy(bboxes)

        if len(bboxes) > 0:
            bboxes = clip_bboxes(bboxes, image_height, image_width)

        return bboxes

    @property
    def has_labels(self):
        return self.labels_exists and len(self.labels.data) > 0

    @property
    def labels_exists(self):
        return self._labels is not None

    @property
    def bboxes_area(self):
        bboxes = self.pascal_voc_bboxes
        return (bboxes[:, 3] - bboxes[:, 1]) * (bboxes[:, 2] - bboxes[:, 0])

    @property
    def has_bboxes(self):
        return self.bboxes_exists and len(self.bboxes.data) > 0

    @property
    def bboxes_exists(self):
        return self._bboxes is not None

    def idx_of_unique_bboxes(self):
        unique_idxs = []
        bboxes_id = [f"{bbox.tolist()}{label}" for (bbox, label) in zip(self.bboxes.data, self.labels.data)]
        bboxes_map = {}
        for i, bbox_id in enumerate(bboxes_id):
            if bbox_id not in bboxes_map:
                bboxes_map[bbox_id] = True
                unique_idxs.append(i)
        return np.array(unique_idxs)

    def idx_of_bboxes_below_pixel_area(self, area=8):
        return np.where(self.bboxes_area < area)[0]

    def idx_of_bboxes_above_or_equal_pixel_area(self, area=8):
        return np.where(self.bboxes_area >= area)[0]

    def remove_duplicate_bboxes(self):
        idxs_to_keep = self.idx_of_unique_bboxes()
        if self.labels is not None and self.bboxes is not None:
            self._labels.data = self._labels.data[idxs_to_keep]
            self._bboxes.data = self._bboxes.data[idxs_to_keep]
        return self

    def remove_bboxes_below_pixel_area(self, area=8):
        idxs_to_keep = self.idx_of_bboxes_above_or_equal_pixel_area(area)
        if self.labels is not None and self.bboxes is not None:
            self._labels.data = self._labels.data[idxs_to_keep]
            self._bboxes.data = self._bboxes.data[idxs_to_keep]
        return self

    def filter_labels_and_bboxes_to_keep(self, labels_to_keep, lazy=True):
        idxs_to_keep = []
        for i, label in enumerate(self._labels.data):
            if label in labels_to_keep:
                idxs_to_keep.append(i)

        self._labels.filter_by_idx(idx=idxs_to_keep, lazy=lazy)
        self._bboxes.filter_by_idx(idx=idxs_to_keep, lazy=lazy)

    def transform_labels(self, transform_label_map, lazy=True):
        self._labels.transform_labels(transform_label_map, lazy=lazy)


class ImageBoundingBoxDetectionSample(_DataMixin, _PlotMixin, _BoundingBoxMixin):
    """
    PASCAL_VOC: [x_min, y_min, x_max, y_max]

    COCO: [x_min, y_min, width, height]

    YOLO: normalized[center_x, center_y, width, height]
    """

    def __init__(self, image, labels=None, bboxes=None, bboxes_format=None, name=None):
        if labels is not None and bboxes is not None:
            assert len(bboxes.data) == len(
                labels.data
            ), f"The number of bboxes ({len(bboxes.data)}) must be the same as the number of labels ({len(labels.data)})"

        assert not ((bboxes is None) ^ (bboxes_format is None)), "Both bboxes and bboxes_format must be defined together, or not defined at all"

        assert bboxes_format in ["PASCAL_VOC", "COCO", "YOLO", None], "bboxes_format needs to be 'PASCAL_VOC', 'COCO', or 'YOLO'"

        self.image = image
        self._labels = labels
        self._bboxes = bboxes
        self._bboxes_format = bboxes_format
        self._convert_to_pascal_voc_bboxes_in_future = False
        self._filter_labels_and_bboxes_to_keep_in_future = False
        self._filter_labels_and_bboxes_to_keep_in_future_args = {}
        self.name = str(uuid4()) if name is None else name

    @classmethod
    def create(
        cls,
        image_data=None,
        image_path=None,
        load_image_fn=imread_rgb,
        labels_data=None,
        labels_path=None,
        load_labels_fn=None,
        bboxes_data=None,
        bboxes_path=None,
        load_bboxes_fn=None,
        bboxes_format=None,
        name=None,
    ):
        if name is None:
            name = Path(image_path).stem if image_path is not None else str(uuid4())

        if image_data is not None:
            image_data = np.array(image_data)

        image = Data(image_data, image_path, load_image_fn)

        if labels_data is None and labels_path is None:
            labels = None
        else:
            if labels_data is not None:
                labels_data = np.array(labels_data)

            labels = Data(labels_data, labels_path, load_labels_fn)

        if bboxes_data is None and bboxes_path is None:
            bboxes = None
        else:
            if bboxes_data is not None:
                bboxes_data = np.array(bboxes_data)
            bboxes = Data(bboxes_data, bboxes_path, load_bboxes_fn)
        return cls(image, labels, bboxes, bboxes_format, name)


lookup = {"ImageBoundingBoxDetectionSample": ImageBoundingBoxDetectionSample}
