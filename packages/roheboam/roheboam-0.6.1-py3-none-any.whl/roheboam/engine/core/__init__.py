from .callbacks import lookup as callbacks_lookup
from .data import lookup as data_lookup
from .losses import lookup as losses_lookup
from .metrics import lookup as metrics_lookup
from .optimizer import lookup as optimizer_lookup
from .scheduler import lookup as scheduler_lookup
from .training import lookup as training_lookup

lookup = {**callbacks_lookup, **data_lookup, **losses_lookup, **metrics_lookup, **optimizer_lookup, **scheduler_lookup, **training_lookup}
