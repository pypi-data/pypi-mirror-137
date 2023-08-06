from .torchvision_fasterrcnn import lookup as torchvision_fasterrcnn_lookup
from .yolov4 import lookup as yolov4_lookup

lookup = {**yolov4_lookup, **torchvision_fasterrcnn_lookup}
