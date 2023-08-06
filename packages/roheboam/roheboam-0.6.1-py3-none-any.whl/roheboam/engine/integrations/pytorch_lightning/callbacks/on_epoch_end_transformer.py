from collections import defaultdict

import torch

from ....core.callbacks import Callback


class OnEpochEndTransformer(Callback):
    """
    Reduces the output from Pytorch Lightning Module from:

    [{"metric_A": "metric_A_sample_1", "metric_B": "metric_B_sample_1", ...}]

    to

    {
        metric_A: mean([metric_A_sample_1, metric_A_sample_2, ...])
        metric_B: mean([metric_B_sample_1, metric_B_sample_2, ...])
    }

    if self.reduce_keys in metric_A

    or:

    {
        metric_A: [metric_A_sample_1, metric_A_sample_2, ...]
    }

    if self.reduce_keys not in metric


    :param Callback: [description]
    :type Callback: [type]
    """

    def __init__(self, reduce_keys=["val_loss", "test_loss"], name=None):
        super().__init__(name)
        self.reduce_keys = reduce_keys

    def _reduce_output(self, all_output):
        reduced_output = defaultdict(list)
        for output in all_output:
            for k, v in output.items():
                reduced_output[k].append(v)
        return {k: torch.mean(torch.stack(v)) if k in self.reduce_keys else v for k, v in reduced_output.items()}

    def on_train_epoch_end(self, context):
        context.all_train_output = self._reduce_output(context.all_train_output)

    def on_validation_epoch_end(self, context):
        context.all_validation_output = self._reduce_output(context.all_validation_output)

    def on_test_epoch_end(self, context):
        context.all_test_output = self._reduce_output(context.all_test_output)


lookup = {"OnEpochEndTransformer": OnEpochEndTransformer}
