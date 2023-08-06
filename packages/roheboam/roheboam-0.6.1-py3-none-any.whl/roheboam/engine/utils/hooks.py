from torch import Tensor

from .convenience import is_listy


class Hooks:
    "Create several hooks on the modules in `ms` with `hook_func`."

    def __init__(self, modules, hook_fn, is_forward=True, detach=True):
        self.hooks = [Hook(m, hook_fn, is_forward, detach) for m in modules]

    def __getitem__(self, i):
        return self.hooks[i]

    def __len__(self):
        return len(self.hooks)

    def __iter__(self):
        return iter(self.hooks)

    @property
    def stored(self):
        return [o.stored for o in self]

    def remove(self):
        "Remove the hooks from the model."
        for h in self.hooks:
            h.remove()

    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        self.remove()


class Hook:
    "Create a hook on `m` with `hook_func`."

    def __init__(self, m, hook_fn, is_forward=True, detach=True):
        self.hook_fn, self.detach, self.stored = hook_fn, detach, None
        register_hook_fn = m.register_forward_hook if is_forward else m.register_backward_hook
        self.hook = register_hook_fn(self.hook_fn_wrapper)
        self.removed = False

    def hook_fn_wrapper(self, module, input, output):
        "Applies `hook_func` to `module`, `input`, `output`."
        if self.detach:
            input = (o.detach() for o in input) if is_listy(input) else input.detach()
            output = (o.detach() for o in output) if is_listy(output) else output.detach()
        self.stored = self.hook_fn(module, input, output)

    def remove(self):
        "Remove the hook from the model."
        if not self.removed:
            self.hook.remove()
            self.removed = True

    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        self.remove()


def hook_output(module, detach=True, grad=False):
    "Return a `Hook` that stores activations of `module` in `self.stored`"
    return Hook(module, _hook_inner, detach=detach, is_forward=not grad)


def hook_outputs(modules, detach=True, grad=False):
    "Return `Hooks` that store activations of all `modules` in `self.stored`"
    return Hooks(modules, _hook_inner, detach=detach, is_forward=not grad)


def _hook_inner(m, i, o):
    return o if isinstance(o, Tensor) else o if is_listy(o) else list(o)


lookup = {"Hooks": Hooks, "Hook": Hook, "hook_output": hook_output, "hook_outputs": hook_outputs}
