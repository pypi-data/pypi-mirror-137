from .box_iou import *
from .box_iou import lookup as box_iou_lookup
from .core import *
from .core import lookup as core_lookup
from .mean_average_precision import *
from .mean_average_precision import lookup as mean_average_precision_lookup

lookup = {**core_lookup, **box_iou_lookup, **mean_average_precision_lookup}
