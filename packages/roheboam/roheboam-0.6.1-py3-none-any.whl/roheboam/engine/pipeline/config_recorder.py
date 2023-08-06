import ast
import inspect
import textwrap
from collections import defaultdict
from uuid import uuid4

from .constants import RESOURCE_KEY, VARIABLE_KEY
from .yaml_loader import Reference, Variable


class ConfigurationNodeRecorder:
    def __init__(self):
        self.recorded_nodes = defaultdict(list)

    @property
    def config(self):
        config = {VARIABLE_KEY: {}, RESOURCE_KEY: {}}
        variables = {}
        for nodes in self.recorded_nodes.values():
            for node in nodes:
                # add the node
                config[RESOURCE_KEY][node.name] = node.config_properties

                # add the variables
                for variable, value in node.variables.items():
                    if variable.is_nested:
                        variable_dict_for_node = {}
                        current_nested_dict = variable_dict_for_node
                        for group_name in variable.variable_groups:
                            current_nested_dict[group_name] = {}
                            current_nested_dict = current_nested_dict[group_name]
                        current_nested_dict[variable.variable_name] = value
                        variables = {**variable_dict_for_node, **variables}
                    else:
                        variables[variable.variable_name] = value
        config[VARIABLE_KEY] = variables
        return config

    @property
    def lookup(self):
        lookup = {}
        for nodes in self.recorded_nodes.values():
            for node in nodes:
                lookup[node.callable_obj.__name__] = node.callable_obj
        return lookup

    def reset_recorded_nodes(self):
        self.recorded_nodes = defaultdict(list)

    def record(self, callable_obj, name=None, tags=[]):
        if name is None:
            name = f"{callable_obj.__name__}_{len(self.recorded_nodes[name])}"
        else:
            name = f"{name}_{self.recorded_nodes[name]}"
        configuration_node = ConfigurationNode(callable_obj, name, tags)
        self.recorded_nodes[name].append(configuration_node)
        return configuration_node


class ConfigurationNode:
    def __init__(self, callable_obj, name=None, tags=[]):
        self.callable_obj = callable_obj
        self.name = name
        self.tags = tags
        self.arguments = {}
        self.variables = {}
        self.output_names = []

    @property
    def config_properties(self):
        return {
            "properties": {"pointer": self.callable_obj.__name__, "arguments": self.arguments, "output_names": self.output_names, "tags": self.tags}
        }

    def __call__(self, *args, **kwargs):
        sig = inspect.signature(self.callable_obj)
        positional_or_keyword_args = [
            param for param in sig.parameters.values() if param.kind == param.POSITIONAL_OR_KEYWORD or param.kind == param.POSITIONAL_ONLY
        ]
        n_positional_or_keyword_args = len(positional_or_keyword_args)

        for arg, param in zip(args, positional_or_keyword_args[:n_positional_or_keyword_args]):
            if self._check_if_variable_is_patched(arg):
                arg_node_name = arg.node_name
                arg_output_name = arg.output_name
                self.arguments[param.name] = Reference(ref_node_name=arg_node_name, output_name=arg_output_name)
            else:
                self.arguments[param.name] = Variable(variable_group=self.name, variable_name=param.name)
                self.variables[Variable(variable_group=self.name, variable_name=param.name)] = arg

        return_values = self.callable_obj(*args, **kwargs)
        output_names = create_output_names(self.callable_obj)
        patched_outputs = []

        for output_name, return_value in zip(output_names, [return_values]):
            patched_outputs.append(
                patch_output_value(
                    return_value,
                    output_name=output_name,
                    node_name=self.name,
                )
            )

        self.output_names = output_names
        return patched_outputs[0] if len(patched_outputs) == 1 else patched_outputs

    def _check_if_variable_is_patched(self, variable):
        try:
            variable.node_name
            variable.output_name
            return True
        except Exception:
            return False


def patch_output_value(value, output_name, node_name):
    new_type = type(
        f"{str(uuid4())}",
        (type(value),),
        {
            "output_name": output_name,
            "node_name": node_name,
        },
    )
    patched_value = new_type(value)
    return patched_value


def create_output_names(f):
    class Visitor(ast.NodeVisitor):
        def visit_Return(self, node):
            self.output_names = []
            if isinstance(node.value, ast.Tuple):
                for i, _ in enumerate(node.value.elts):
                    self.output_names.append(str(i))
            else:
                self.output_names.append("0")
            self.generic_visit(node)

    visitor = Visitor()
    visitor.visit(ast.parse(textwrap.dedent(inspect.getsource(f))))
    return visitor.output_names
