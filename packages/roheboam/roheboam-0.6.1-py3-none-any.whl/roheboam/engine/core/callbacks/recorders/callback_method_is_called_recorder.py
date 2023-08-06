from ..callback import Callback


class CallbackMethodIsCalledRecorder(Callback):
    def __init__(self, name=None):
        super().__init__(name)
        self.method_is_called = {
            "on_setup": True,
            "on_init_begin": False,
            "on_init_end": False,
            "on_train_begin": False,
            "on_train_epoch_begin": False,
            "on_train_batch_begin": False,
            "on_train_loss_begin": False,
            "on_backward_begin": False,
            "on_backward_end": False,
            "on_train_step_end": False,
            "on_train_batch_end": False,
            "on_validation_begin": False,
            "on_validation_epoch_begin": False,
            "on_validation_batch_begin": False,
            "on_validation_loss_begin": False,
            "on_validation_step_end": False,
            "on_validation_batch_end": False,
            "on_validation_epoch_end": False,
            "on_validation_end": False,
            "on_train_epoch_end": False,
            "on_train_end": False,
            "on_test_begin": False,
            "on_test_epoch_begin": False,
            "on_test_batch_begin": False,
            "on_test_loss_begin": False,
            "on_test_step_end": False,
            "on_test_batch_end": False,
            "on_test_epoch_end": False,
            "on_test_end": False,
            "on_teardown": False,
        }

    def on_setup(self, context):
        self.method_is_called["on_setup"] = True

    def on_init_begin(self, context):
        self.method_is_called["on_init_begin"] = True

    def on_init_end(self, context):
        self.method_is_called["on_init_end"] = True

    def on_train_begin(self, context):
        self.method_is_called["on_train_begin"] = True

    def on_train_epoch_begin(self, context):
        self.method_is_called["on_train_epoch_begin"] = True

    def on_train_batch_begin(self, context):
        self.method_is_called["on_train_batch_begin"] = True

    def on_train_loss_begin(self, context):
        self.method_is_called["on_train_loss_begin"] = True

    def on_backward_begin(self, context):
        self.method_is_called["on_backward_begin"] = True

    def on_backward_end(self, context):
        self.method_is_called["on_backward_end"] = True

    def on_train_step_end(self, context):
        self.method_is_called["on_train_step_end"] = True

    def on_train_batch_end(self, context):
        self.method_is_called["on_train_batch_end"] = True

    def on_validation_begin(self, context):
        self.method_is_called["on_validation_begin"] = True

    def on_validation_epoch_begin(self, context):
        self.method_is_called["on_validation_epoch_begin"] = True

    def on_validation_batch_begin(self, context):
        self.method_is_called["on_validation_batch_begin"] = True

    def on_validation_loss_begin(self, context):
        self.method_is_called["on_validation_loss_begin"] = True

    def on_validation_step_end(self, context):
        self.method_is_called["on_validation_step_end"] = True

    def on_validation_batch_end(self, context):
        self.method_is_called["on_validation_batch_end"] = True

    def on_validation_epoch_end(self, context):
        self.method_is_called["on_validation_epoch_end"] = True

    def on_validation_end(self, context):
        self.method_is_called["on_validation_end"] = True

    def on_train_epoch_end(self, context):
        self.method_is_called["on_train_epoch_end"] = True

    def on_train_end(self, context):
        self.method_is_called["on_train_end"] = True

    def on_test_begin(self, context):
        self.method_is_called["on_test_begin"] = True

    def on_test_epoch_begin(self, context):
        self.method_is_called["on_test_epoch_begin"] = True

    def on_test_batch_begin(self, context):
        self.method_is_called["on_test_batch_begin"] = True

    def on_test_loss_begin(self, context):
        self.method_is_called["on_test_loss_begin"] = True

    def on_test_step_end(self, context):
        self.method_is_called["on_test_step_end"] = True

    def on_test_batch_end(self, context):
        self.method_is_called["on_test_batch_end"] = True

    def on_test_epoch_end(self, context):
        self.method_is_called["on_test_epoch_end"] = True

    def on_test_end(self, context):
        self.method_is_called["on_test_end"] = True

    def on_teardown(self, context):
        self.method_is_called["on_teardown"] = True


CallbackMethodIsCalled = CallbackMethodIsCalledRecorder
