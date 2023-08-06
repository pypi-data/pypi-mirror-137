from dataclasses import dataclass

import yaml


class RoheboamYamlLoader(yaml.SafeLoader):
    pass


class RoheboamYamlDumper(yaml.SafeDumper):
    pass


@dataclass
class Variable:
    variable_group: str
    variable_name: str

    @property
    def is_nested(self):
        return self.variable_group is not None

    @property
    def variable_groups(self):
        return [subgroup_name for subgroup_name in self.variable_group.split(".")]

    def __hash__(self):
        return hash(f"{self.variable_name}{self.variable_group}")

    def __eq__(self, other):
        if not isinstance(self, type(other)):
            return False

        if self.variable_group != other.variable_group:
            return False

        return self.variable_name == other.variable_name


def var_constructor(loader, node):
    if "." in node.value:
        *variable_group, variable_name = node.value.split(".")
        return Variable(variable_group=".".join(variable_group), variable_name=variable_name)
    else:
        return Variable(variable_group=None, variable_name=node.value)


def var_representer(dumper: RoheboamYamlDumper, variable: Variable):
    if variable.is_nested:
        value = f"{variable.variable_group}.{variable.variable_name}"
    else:
        value = f"{variable.variable_name}"
    return dumper.represent_scalar("!Var", f"{value}")


@dataclass
class Reference:
    ref_node_name: str
    output_name: str


def ref_constructor(loader, node):
    ref_node_name_and_output_name = node.value.split(".")
    assert (
        len(ref_node_name_and_output_name) == 2
    ), f"No output is being accessed for resource: '{node.tag} {node.value}' please search \
        through the configuration file using '{node.tag} {node.value}' to add an access to that resource"
    ref_node_name, output_name = ref_node_name_and_output_name
    return Reference(ref_node_name=ref_node_name, output_name=output_name)


def ref_representer(dumper, data):
    value = f"{data.ref_node_name}.{data.output_name}"
    return dumper.represent_scalar("!Ref", f"{value}")


RoheboamYamlLoader.add_constructor("!Var", var_constructor)
RoheboamYamlLoader.add_constructor("!Ref", ref_constructor)

RoheboamYamlDumper.add_representer(Variable, var_representer)
RoheboamYamlDumper.add_representer(Reference, ref_representer)
