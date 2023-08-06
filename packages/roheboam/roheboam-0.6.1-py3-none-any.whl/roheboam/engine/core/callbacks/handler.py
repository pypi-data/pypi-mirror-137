from abc import ABC
from enum import Enum, IntEnum

from ...utils.convenience import debug_log_on_call


class CallbackHandler:
    @debug_log_on_call
    def __init__(self, callbacks):
        self.context = CallbackHandlerContext()
        self.callbacks = callbacks
        self.callbacks = sorted(self.callbacks, key=lambda cb: getattr(cb, "_order", 0))

    def get_callback_by_name(self, name):
        for cb in self.callbacks:
            if cb.name == name:
                return cb

        for cb in self.callbacks:
            if name in cb.name:
                return cb

        return None

    def set_context_value(self, key, value):
        self.context[key] = value

    def get_context_value(self, key):
        return self.context[key]

    @debug_log_on_call
    def on_setup(self):
        for cb in self.callbacks:
            cb.on_setup(self.context)

    @debug_log_on_call
    def on_init_begin(self):
        for cb in self.callbacks:
            cb.on_init_begin(self.context)

    @debug_log_on_call
    def on_init_end(self):
        for cb in self.callbacks:
            cb.on_init_end(self.context)

    @debug_log_on_call
    def on_train_begin(self):
        for cb in self.callbacks:
            cb.on_train_begin(self.context)

    @debug_log_on_call
    def on_train_epoch_begin(self):
        self.context.current_phase = Phase.TRAIN
        for cb in self.callbacks:
            cb.on_train_epoch_begin(self.context)

    @debug_log_on_call
    def on_train_batch_begin(self):
        for cb in self.callbacks:
            cb.on_train_batch_begin(self.context)
        return self.context.train_batch

    @debug_log_on_call
    def on_train_loss_begin(self):
        for cb in self.callbacks:
            cb.on_train_loss_begin(self.context)
        return self.context.train_prediction

    @debug_log_on_call
    def on_train_step_end(self):
        for cb in self.callbacks:
            cb.on_train_step_end(self.context)
        return self.context.train_output

    @debug_log_on_call
    def on_backward_begin(self):
        for cb in self.callbacks:
            cb.on_backward_begin(self.context)
        return self.context.train_loss

    @debug_log_on_call
    def on_backward_end(self):
        for cb in self.callbacks:
            cb.on_backward_end(self.context)

    @debug_log_on_call
    def on_train_batch_end(self):
        for cb in self.callbacks:
            cb.on_train_batch_end(self.context)

    @debug_log_on_call
    def on_validation_begin(self):
        for cb in self.callbacks:
            cb.on_validation_begin(self.context)

    @debug_log_on_call
    def on_validation_epoch_begin(self):
        self.context.current_phase = Phase.VALIDATION
        for cb in self.callbacks:
            cb.on_validation_epoch_begin(self.context)

    @debug_log_on_call
    def on_validation_batch_begin(self):
        for cb in self.callbacks:
            cb.on_validation_batch_begin(self.context)
        return self.context.validation_batch

    @debug_log_on_call
    def on_validation_loss_begin(self):
        for cb in self.callbacks:
            cb.on_validation_loss_begin(self.context)
        return self.context.validation_prediction

    @debug_log_on_call
    def on_validation_step_end(self):
        for cb in self.callbacks:
            cb.on_validation_step_end(self.context)
        return self.context.validation_output

    @debug_log_on_call
    def on_validation_batch_end(self):
        for cb in self.callbacks:
            cb.on_validation_batch_end(self.context)

    @debug_log_on_call
    def on_validation_epoch_end(self):
        for cb in self.callbacks:
            cb.on_validation_epoch_end(self.context)
        return self.context.all_validation_output

    @debug_log_on_call
    def on_validation_end(self):
        for cb in self.callbacks:
            cb.on_validation_end(self.context)

    @debug_log_on_call
    def on_train_epoch_end(self):
        for cb in self.callbacks:
            cb.on_train_epoch_end(self.context)
        return self.context.all_train_output

    @debug_log_on_call
    def on_train_end(self):
        for cb in self.callbacks:
            cb.on_train_end(self.context)

    @debug_log_on_call
    def on_test_begin(self):
        for cb in self.callbacks:
            cb.on_test_begin(self.context)

    @debug_log_on_call
    def on_test_epoch_begin(self):
        self.context.current_phase = Phase.TEST
        for cb in self.callbacks:
            cb.on_test_epoch_begin(self.context)

    @debug_log_on_call
    def on_test_batch_begin(self):
        for cb in self.callbacks:
            cb.on_test_batch_begin(self.context)
        return self.context.test_batch

    @debug_log_on_call
    def on_test_loss_begin(self):
        for cb in self.callbacks:
            cb.on_test_loss_begin(self.context)
        return self.context.test_prediction

    @debug_log_on_call
    def on_test_step_end(self):
        for cb in self.callbacks:
            cb.on_test_step_end(self.context)
        return self.context.test_output

    @debug_log_on_call
    def on_test_batch_end(self):
        for cb in self.callbacks:
            cb.on_test_batch_end(self.context)

    @debug_log_on_call
    def on_test_epoch_end(self):
        for cb in self.callbacks:
            cb.on_test_epoch_end(self.context)
        return self.context.all_test_output

    @debug_log_on_call
    def on_test_end(self):
        for cb in self.callbacks:
            cb.on_test_end(self.context)

    @debug_log_on_call
    def on_teardown(self):
        for cb in self.callbacks:
            cb.on_teardown(self.context)


Phase = IntEnum("Phase", "TRAIN VALIDATION TEST")
CallbackHandlerContextValues = IntEnum(
    "CallbackHandlerContextValues",
    "SAVE_DIRECTORY LOSS MODEL TRAINER TRAIN_BATCH TRAIN_PREDICTION TRAIN_LOSS TRAIN_METRIC TRAIN_OUTPUT ALL_TRAIN_OUTPUT \
    VALIDATION_BATCH VALIDATION_PREDICTION VALIDATION_LOSS VALIDATION_METRIC VALIDATION_OUTPUT ALL_VALIDATION_OUTPUT \
    TEST_BATCH TEST_PREDICTION TEST_LOSS TEST_METRIC TEST_OUTPUT ALL_TEST_OUTPUT CURRENT_EPOCH CURRENT_PHASE CURRENT_STEP",
)


class CallbackHandlerContext(dict):
    def __init__(self):
        self.current_epoch = 0

    @property
    def save_directory(self):
        return self.get(CallbackHandlerContextValues.SAVE_DIRECTORY)

    @save_directory.setter
    def save_directory(self, value):
        self[CallbackHandlerContextValues.SAVE_DIRECTORY] = value

    @property
    def loss(self):
        return self.get(CallbackHandlerContextValues.LOSS)

    @property
    def model(self):
        return self.get(CallbackHandlerContextValues.MODEL)

    @property
    def trainer(self):
        return self.get(CallbackHandlerContextValues.TRAINER)

    @property
    def current_phase(self):
        return self.get(CallbackHandlerContextValues.CURRENT_PHASE)

    @current_phase.setter
    def current_phase(self, value):
        self[CallbackHandlerContextValues.CURRENT_PHASE] = value

    @property
    def current_epoch(self):
        return self.get(CallbackHandlerContextValues.CURRENT_EPOCH)

    @current_epoch.setter
    def current_epoch(self, value):
        self[CallbackHandlerContextValues.CURRENT_EPOCH] = value

    @property
    def current_step(self):
        return self.get(CallbackHandlerContextValues.CURRENT_STEP)

    @current_step.setter
    def current_step(self, value):
        self[CallbackHandlerContextValues.CURRENT_STEP] = value

    @property
    def train_batch(self):
        return self.get(CallbackHandlerContextValues.TRAIN_BATCH)

    @train_batch.setter
    def train_batch(self, value):
        self[CallbackHandlerContextValues.TRAIN_BATCH] = value

    @property
    def train_prediction(self):
        return self.get(CallbackHandlerContextValues.TRAIN_PREDICTION)

    @train_prediction.setter
    def train_prediction(self, value):
        self[CallbackHandlerContextValues.TRAIN_PREDICTION] = value

    @property
    def train_loss(self):
        return self.get(CallbackHandlerContextValues.TRAIN_LOSS)

    @train_loss.setter
    def train_loss(self, value):
        self[CallbackHandlerContextValues.TRAIN_LOSS] = value

    @property
    def train_metric(self):
        return self.get(CallbackHandlerContextValues.TRAIN_METRIC)

    @train_metric.setter
    def train_metric(self, value):
        self[CallbackHandlerContextValues.TRAIN_METRIC] = value

    @property
    def train_output(self):
        return self.get(CallbackHandlerContextValues.TRAIN_OUTPUT)

    @train_output.setter
    def train_output(self, value):
        self[CallbackHandlerContextValues.TRAIN_OUTPUT] = value

    @property
    def all_train_output(self):
        return self.get(CallbackHandlerContextValues.ALL_TRAIN_OUTPUT)

    @all_train_output.setter
    def all_train_output(self, value):
        self[CallbackHandlerContextValues.ALL_TRAIN_OUTPUT] = value

    @property
    def validation_batch(self):
        return self.get(CallbackHandlerContextValues.VALIDATION_BATCH)

    @validation_batch.setter
    def validation_batch(self, value):
        self[CallbackHandlerContextValues.VALIDATION_BATCH] = value

    @property
    def validation_prediction(self):
        return self.get(CallbackHandlerContextValues.VALIDATION_PREDICTION)

    @validation_prediction.setter
    def validation_prediction(self, value):
        self[CallbackHandlerContextValues.VALIDATION_PREDICTION] = value

    @property
    def validation_loss(self):
        return self.get(CallbackHandlerContextValues.VALIDATION_LOSS)

    @validation_loss.setter
    def validation_loss(self, value):
        self[CallbackHandlerContextValues.VALIDATION_LOSS] = value

    @property
    def validation_metric(self):
        return self.get(CallbackHandlerContextValues.VALIDATION_METRIC)

    @validation_metric.setter
    def validation_metric(self, value):
        self[CallbackHandlerContextValues.VALIDATION_METRIC] = value

    @property
    def validation_output(self):
        return self.get(CallbackHandlerContextValues.VALIDATION_OUTPUT)

    @validation_output.setter
    def validation_output(self, value):
        self[CallbackHandlerContextValues.VALIDATION_OUTPUT] = value

    @property
    def all_validation_output(self):
        return self.get(CallbackHandlerContextValues.ALL_VALIDATION_OUTPUT)

    @all_validation_output.setter
    def all_validation_output(self, value):
        self[CallbackHandlerContextValues.ALL_VALIDATION_OUTPUT] = value

    @property
    def test_batch(self):
        return self.get(CallbackHandlerContextValues.TEST_BATCH)

    @test_batch.setter
    def test_batch(self, value):
        self[CallbackHandlerContextValues.TEST_BATCH] = value

    @property
    def test_prediction(self):
        return self.get(CallbackHandlerContextValues.TEST_PREDICTION)

    @test_prediction.setter
    def test_prediction(self, value):
        self[CallbackHandlerContextValues.TEST_PREDICTION] = value

    @property
    def test_loss(self):
        return self.get(CallbackHandlerContextValues.TEST_LOSS)

    @test_loss.setter
    def test_loss(self, value):
        self[CallbackHandlerContextValues.TEST_LOSS] = value

    @property
    def test_metric(self):
        return self.get(CallbackHandlerContextValues.TEST_METRIC)

    @test_metric.setter
    def test_metric(self, value):
        self[CallbackHandlerContextValues.TEST_METRIC] = value

    @property
    def test_output(self):
        return self.get(CallbackHandlerContextValues.TEST_OUTPUT)

    @test_output.setter
    def test_output(self, value):
        self[CallbackHandlerContextValues.TEST_OUTPUT] = value

    @property
    def all_test_output(self):
        return self.get(CallbackHandlerContextValues.ALL_TEST_OUTPUT)

    @all_test_output.setter
    def all_test_output(self, value):
        self[CallbackHandlerContextValues.ALL_TEST_OUTPUT] = value
