from .adam import Adam
from .ranger import Ranger
from .sgd import SGD

lookup = {"Adam": Adam, "Ranger": Ranger, "SGD": SGD}
