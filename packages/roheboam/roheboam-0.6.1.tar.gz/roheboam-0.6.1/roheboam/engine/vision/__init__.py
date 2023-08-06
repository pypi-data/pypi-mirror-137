from .core import *
from .core import lookup as core_lookup
from .tasks import *
from .tasks import lookup as tasks_lookup
from .utils import *
from .utils import lookup as utils_lookup

lookup = {**core_lookup, **tasks_lookup, **utils_lookup}
