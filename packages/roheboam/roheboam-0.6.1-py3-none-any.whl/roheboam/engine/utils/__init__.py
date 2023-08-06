from .conda import lookup as conda_lookup
from .convenience import lookup as convenience_lookup
from .hooks import lookup as hooks_lookup
from .interfaces import lookup as interfaces_lookup
from .model import lookup as models_lookup
from .saving import lookup as saving_lookup
from .testing import lookup as testing_lookup
from .training import lookup as training_lookup

lookup = {
    **conda_lookup,
    **convenience_lookup,
    **hooks_lookup,
    **interfaces_lookup,
    **models_lookup,
    **saving_lookup,
    **testing_lookup,
    **training_lookup,
}
