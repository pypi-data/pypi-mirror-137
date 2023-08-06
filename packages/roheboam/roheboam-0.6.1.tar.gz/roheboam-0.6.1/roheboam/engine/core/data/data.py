from abc import ABC
from functools import partial

import numpy as np

from ...utils.convenience import is_listy


class Data(ABC):
    def __init__(self, data=None, path=None, load_fn=None, name=None, should_cache=False, fns_to_run=None):
        if data is None and path is None:
            assert False, "Both the data and the path to the data can't be none, you must define one"

        if path is not None:
            assert load_fn is not None, "A path is provided, so a function must be defined to load it"

        self._data = data
        self.path = path
        self.load_fn = load_fn
        self.name = name
        self.should_cache = should_cache
        if fns_to_run is None:
            self.fns_to_run = []

    @property
    def data(self):
        return self._load_if_needed_then_cache()

    def run_fns_to_run(self):
        while len(self.fns_to_run) > 0:
            self.fns_to_run.pop(0)()

    @data.setter
    def data(self, value):
        self._data = value

    def filter_by_idx(self, idx, lazy=True):
        if len(idx) == 0:
            self._data = np.array([])
            return

        if not lazy:
            self._data = self.data[idx]
            return

        self.fns_to_run.append(partial(self.filter_by_idx, idx=idx, lazy=False))

    def transform_labels(self, transform_label_map, lazy=True):
        if not lazy:
            self._data = np.array([transform_label_map[d] for d in self.data])
            return

        self.fns_to_run.append(partial(self.transform_labels, transform_label_map=transform_label_map, lazy=False))

    def _load_if_needed_then_cache(self):
        if self._data is None:
            if is_listy(self.path):
                data = [self.load_fn(p) for p in self.path]
            else:
                data = self.load_fn(self.path)
            if self.should_cache:
                self._data = data
            return data
        else:
            return self._data


lookup = {"Data": Data}
