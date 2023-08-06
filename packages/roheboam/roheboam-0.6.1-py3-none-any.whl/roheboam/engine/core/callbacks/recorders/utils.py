from collections import defaultdict

from ..handler import Phase


class Storage:
    def __init__(self):
        self._storage = defaultdict(list)

    def read(self, phase, epoch, key):
        return self._storage[(phase, epoch, key)]

    def write(self, phase, epoch, key, data=[]):
        assert isinstance(data, list) or isinstance(data, tuple)
        self._storage[(phase, epoch, key)].extend(data)


class ShouldRecordMixin:
    def _should_store(self, phase, epoch, step):
        if step == 0 or step % self.record_every_n_steps == 0:
            return True
        if phase == Phase.VALIDATION and self.record_on_validation:
            return True
        if phase == Phase.TEST and self.record_on_test:
            return True
        return False
