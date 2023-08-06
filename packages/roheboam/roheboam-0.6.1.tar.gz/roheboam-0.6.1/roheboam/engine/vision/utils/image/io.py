from pathlib import Path

import cv2
import numpy as np

HAS_LIBVIPS = True
try:
    import pyvips
except Exception:
    HAS_LIBVIPS = False


def imread_rgb(path):
    if HAS_LIBVIPS:
        image = pyvips.Image.new_from_file(str(path), access="sequential")
        mem_img = image.write_to_memory()
        return np.frombuffer(mem_img, dtype=np.uint8).reshape(image.height, image.width, 3)
    else:
        return np.array(cv2.cvtColor(cv2.imread(str(path), cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGB))


def imread_grayscale(path):
    if HAS_LIBVIPS:
        image = pyvips.Image.new_from_file(str(path), access="sequential")
        mem_img = image.write_to_memory()
        return np.frombuffer(mem_img, dtype=np.uint8).reshape(image.height, image.width)
    else:
        return np.array(cv2.imread(str(path), cv2.IMREAD_GRAYSCALE))


def imwrite(path, image):
    Path(path).parent.mkdir(exist_ok=True, parents=True)
    cv2.imwrite(path, image)


lookup = {
    "imread_rgb": imread_rgb,
    "imread_grayscale": imread_grayscale,
    "imwrite": imwrite,
}
