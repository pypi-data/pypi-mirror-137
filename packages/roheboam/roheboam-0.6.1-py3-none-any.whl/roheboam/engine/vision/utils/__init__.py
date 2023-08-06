from .bbox import *
from .bbox import lookup as bbox_lookup
from .image import *
from .image import lookup as image_lookup
from .normalization import *
from .normalization import lookup as normalization_lookup
from .rle import *
from .rle import lookup as rle_lookup
from .transforms import *
from .transforms import lookup as transform_lookup
from .u_net_weight_map import *

lookup = {**bbox_lookup, **image_lookup, **normalization_lookup, **rle_lookup, **transform_lookup}
