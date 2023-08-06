from .label_statistics import *
from .label_statistics import lookup as label_statistics_lookup
from .mean_average_precision import *
from .mean_average_precision import lookup as mean_average_precision_lookup

lookup = {**mean_average_precision_lookup, **label_statistics_lookup}
