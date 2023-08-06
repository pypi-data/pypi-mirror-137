from .image_bounding_box_detection import lookup as image_bounding_box_detection_lookup
from .image_classification import lookup as image_classification_lookup
from .image_segmentation import lookup as image_segmentation_lookup

lookup = {**image_bounding_box_detection_lookup, **image_segmentation_lookup, **image_classification_lookup}
