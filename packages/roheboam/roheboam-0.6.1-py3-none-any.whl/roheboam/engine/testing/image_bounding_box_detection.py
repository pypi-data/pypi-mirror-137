import random

import numpy as np


def create_black_image_data(width, height, n_channels, torch_format=True, type=np.uint8):
    image = np.stack([np.zeros((height, width))] * n_channels)

    if torch_format:
        image = image.transpose(1, 2, 0)

    return image.astype(type)


def create_random_labels_data(n_labels, n_classes):
    return np.array([random.randint(0, n_classes) for _ in range(n_labels)])


def create_random_yolo_bboxes_data(n_bboxes):
    bboxes = []
    for _ in range(n_bboxes):
        center_x = random.random()
        center_y = random.random()
        width = abs(1 - center_x) * random.random()
        height = abs(1 - center_y) * random.random()
        bboxes.append([center_x, center_y, width, height])
    return np.array(bboxes)


def create_random_pascal_bboxes_data(max_width, max_height, n_bboxes):
    bboxes = []
    for _ in range(n_bboxes):
        x1 = random.random() * max_width
        y1 = random.random() * max_height
        x2 = abs(1 - x1) * random.random() * max_width
        y2 = abs(1 - y1) * random.random() * max_height
        bboxes.append([x1, y1, x2, y2])
    return np.array(bboxes)
