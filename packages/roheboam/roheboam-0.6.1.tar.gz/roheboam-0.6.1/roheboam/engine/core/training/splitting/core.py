from abc import ABC, abstractmethod

from sklearn.model_selection import ShuffleSplit as SKLearnShuffleSplit
from sklearn.model_selection import (
    StratifiedShuffleSplit as SKLearnStratifiedShuffleSplit,
)


class Splitter(ABC):
    @abstractmethod
    def split(self):
        pass


class ShuffleSplit(SKLearnShuffleSplit):
    def __init__(self, X, n_splits=10, test_size=None, train_size=None, random_state=None):
        self.X = X
        self.splitter = SKLearnShuffleSplit(n_splits=n_splits, test_size=test_size, train_size=train_size, random_state=random_state)

    def split(self):
        for (train_idx, val_idx) in self.splitter.split(self.X):
            yield train_idx, val_idx


class StratifiedShuffleSplit(SKLearnStratifiedShuffleSplit):
    def __init__(self, X, y, n_splits=10, test_size=None, train_size=None, random_state=None):
        self.X = X
        self.y = y
        self.splitter = SKLearnShuffleSplit(n_splits=n_splits, test_size=test_size, train_size=train_size, random_state=random_state)

    def split(self):
        for (train_idx, val_idx) in self.splitter.split(self.X, self.y):
            yield train_idx, val_idx
