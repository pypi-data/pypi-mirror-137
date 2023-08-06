from abc import ABC
from uuid import uuid4


class Callback(ABC):
    _order = 0

    def __init__(self, name=None):
        if name is None:
            self.name = f"{self.__class__.__name__}-{str(uuid4())[:4]}"
        else:
            self.name = name

    def on_setup(self, context):
        pass

    def on_init_begin(self, context):
        pass

    def on_init_end(self, context):
        pass

    def on_train_begin(self, context):
        pass

    def on_train_epoch_begin(self, context):
        pass

    def on_train_batch_begin(self, context):
        pass

    def on_train_loss_begin(self, context):
        pass

    def on_backward_begin(self, context):
        pass

    def on_backward_end(self, context):
        pass

    def on_train_step_end(self, context):
        pass

    def on_train_batch_end(self, context):
        pass

    def on_validation_begin(self, context):
        pass

    def on_validation_epoch_begin(self, context):
        pass

    def on_validation_batch_begin(self, context):
        pass

    def on_validation_loss_begin(self, context):
        pass

    def on_validation_step_end(self, context):
        pass

    def on_validation_batch_end(self, context):
        pass

    def on_validation_epoch_end(self, context):
        pass

    def on_validation_end(self, context):
        pass

    def on_train_epoch_end(self, context):
        pass

    def on_train_end(self, context):
        pass

    def on_test_begin(self, context):
        pass

    def on_test_epoch_begin(self, context):
        pass

    def on_test_batch_begin(self, context):
        pass

    def on_test_loss_begin(self, context):
        pass

    def on_test_step_end(self, context):
        pass

    def on_test_batch_end(self, context):
        pass

    def on_test_epoch_end(self, context):
        pass

    def on_test_end(self, context):
        pass

    def on_teardown(self, context):
        pass
