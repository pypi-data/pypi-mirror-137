import os

import pytorch_lightning as pl

from ...integrations.pytorch_lightning.adapters import (
    PytorchLightningCallbacksToCallbackHandlerAdapter,
)


def create_pytorch_lightning_trainer(
    callback_handler,
    gpus=1,
    max_epochs=1,
    checkpoint_callback=None,
    resume_from_checkpoint=None,
    gradient_clip_val=0,
    num_sanity_val_steps=0,
):

    return pl.Trainer(
        callbacks=[PytorchLightningCallbacksToCallbackHandlerAdapter(callback_handler)],
        gpus=gpus,
        max_epochs=max_epochs,
        resume_from_checkpoint=resume_from_checkpoint,
        checkpoint_callback=checkpoint_callback,
        gradient_clip_val=gradient_clip_val,
        num_sanity_val_steps=num_sanity_val_steps,
        logger=None,
    )


lookup = {"create_pytorch_lightning_trainer": create_pytorch_lightning_trainer}
