import torch.nn as nn


def cadene_change_last_linear(model_creator, out_features):
    model = model_creator()
    dim_feats = model.last_linear.in_features
    model.last_linear = nn.Linear(dim_feats, out_features)
    return model
