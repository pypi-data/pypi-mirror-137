from copy import deepcopy

import cv2
import matplotlib.pyplot as plt
import numpy as np


def plot_image_grid(images, titles=None, ncols=None, cmap="gray", figsize=None):
    if titles is not None:
        assert len(images) == len(titles)
    if not ncols:
        factors = [i for i in range(1, len(images) + 1) if len(images) % i == 0]
        ncols = factors[len(factors) // 2] if len(factors) else len(images) // 4 + 1
    nrows = int(len(images) / ncols) + int(len(images) % ncols)
    imgs = [images[i] if len(images) > i else None for i in range(nrows * ncols)]

    if figsize is None:
        figsize = (3 * ncols, 2 * nrows)
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes = axes.flatten()[: len(imgs)]
    for i, (img, ax) in enumerate(zip(imgs, axes.flatten())):
        if len(img.shape) > 2 and img.shape[2] == 1:
            img = img.squeeze()
        ax.imshow(img, cmap=cmap)
        if titles is not None:
            ax.set_title(titles[i])
    fig.tight_layout()


def plot_polygons_on_image(image, polygons, is_closed=True, color=(0, 255, 0), thickness=1):
    """Plot bbox on an image

    :param image: np.array with H x W x C
    :type image: list
    :param bboxes: list of polygons in the OpenCV format: [[x1, y1], [x2, y2], ...]
    :type bboxes: list
    :param color: [description], defaults to (0, 255, 0)
    :type color: tuple, optional
    :param thickness: [description], defaults to 1
    :type thickness: int, optional
    """
    from . import is_rgb

    assert is_rgb(image), "Please make sure that the image is RGB"

    image = deepcopy(image)
    for polygon in [polygons]:
        cv2.polylines(image, [np.array(polygon)], is_closed, color, thickness)
    return image


def plot_bounding_boxes_on_image_with_label(image, bboxes, labels, label_bbox_metas=None):
    """Plot bbox with labels on image

    :param image: np.array with H x W x C
    :type image: list
    :param bboxes: list of bbox in the pascal_format: [x_min, y_min, x_max, y_max]
    :type bboxes: list
    :param labels: list of labels for each bbox
    :type labels: list
    :param label_bbox_metas: list of dicts {label: <int>, color: (r, g, b), thickness: <int>}
    :type label_bbox_metas: list
    """
    labels = [int(label) for label in deepcopy(labels)]

    if label_bbox_metas is None:
        rgb_map = _generate_default_rgb_map()
        label_bbox_metas = [{"label": label, "name": str(label), "color": rgb_map[label % len(rgb_map)], "thickness": 3} for label in labels]

    # deepcopy and avoid https://github.com/opencv/opencv/issues/18120
    image = np.ones(image.shape, np.uint8) * image

    for bbox, label_to_plot in zip(bboxes, labels):
        x_min, y_min, x_max, y_max = [int(f) for f in bbox]
        label_bbox_meta = [label for label in label_bbox_metas if label["label"] == label_to_plot][0]
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), label_bbox_meta["color"], label_bbox_meta["thickness"])
        cv2.putText(
            image, label_bbox_meta["name"], (x_min, y_min - 2), 0, 1, [225, 255, 255], thickness=label_bbox_meta["thickness"], lineType=cv2.LINE_AA
        )
    #         cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
    return image


def _generate_default_rgb_map():
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    # https://stackoverflow.com/questions/51350872/python-from-color-name-to-rgb
    hex2rgb = lambda h: tuple(int(h[1 + i : 1 + i + 2], 16) for i in (0, 2, 4))
    return [hex2rgb(h) for h in prop_cycle.by_key()["color"]]


def plot_bounding_boxes_on_image(image, bboxes, color=(0, 255, 0), thickness=1):
    """Plot bbox on an image

    :param image: np.array with H x W x C
    :type image: list
    :param bboxes: list of bbox in the pascal_format: [x_min, y_min, x_max, y_max]
    :type bboxes: list
    :param color: [description], defaults to (0, 255, 0)
    :type color: tuple, optional
    :param thickness: [description], defaults to 1
    :type thickness: int, optional
    """

    from . import is_rgb

    assert is_rgb(image), "Please make sure that the image is RGB"

    # deepcopy and avoid https://github.com/opencv/opencv/issues/18120
    image = np.ones(image.shape, np.uint8) * image
    for bbox in bboxes:
        x_min, y_min, x_max, y_max = bbox
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)
    return image


def plot_mask_on_image(image, mask, image_alpha=0.2):
    from . import to_rgb, to_uint8_image

    return cv2.addWeighted(to_uint8_image(image), image_alpha, to_uint8_image(to_rgb(mask)), 1 - image_alpha, 0)


lookup = {
    "plot_image_grid": plot_image_grid,
    "plot_polygons_on_image": plot_polygons_on_image,
    "plot_bounding_boxes_on_image_with_label": plot_bounding_boxes_on_image_with_label,
    "plot_bounding_boxes_on_image": plot_bounding_boxes_on_image,
    "plot_mask_on_image": plot_mask_on_image,
}
