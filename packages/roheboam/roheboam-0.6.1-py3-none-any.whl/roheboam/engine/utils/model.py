import torch


def model_sizes(m, size=(256, 256), full=True):
    "Pass a dummy input through the model to get the various sizes."
    from .hooks import hook_outputs

    hooks = hook_outputs(m)
    ch_in = in_channels(m)
    x = torch.zeros(1, ch_in, *size)
    x = m.eval()(x)
    res = [o.stored.shape for o in hooks]
    if not full:
        hooks.remove()
    return res, x, hooks if full else res


def in_channels(m):
    "Return the shape of the first weight layer in `m`."
    for layer in flatten_model(m):
        if hasattr(layer, "weight"):
            return layer.weight.shape[1]
    raise Exception("No weight layer")


def flatten_model(m):
    return sum(map(flatten_model, m.children()), []) if num_children(m) else [m]


def num_children(m):
    return len(children(m))


def children(m):
    return list(m.children())


lookup = {
    "model_sizes": model_sizes,
    "in_channels": in_channels,
    "flatten_model": flatten_model,
    "num_children": num_children,
    "children": children,
}
