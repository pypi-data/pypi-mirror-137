import functools
from enum import Enum
from pprint import pformat
from textwrap import dedent

from roheboam.engine.logger import logger

from .constants import SHOULD_REMOVE_ARGUMENT
from .graph_construction import Reference


class NodeRemoveMode(Enum):
    AUTO = 0
    ONLY = 1
    PROPAGATE = 2


class Node:
    def __init__(
        self, name, references, pointer, partial, arguments, output_names, tags=[], should_remove=False, remove_mode=NodeRemoveMode.PROPAGATE
    ):
        self.name = name
        self.references = references
        self.referenced_by = []
        self.pointer = pointer
        self.partial = partial
        self.arguments = arguments
        self.output_names = output_names
        self.tags = tags
        self.should_remove = should_remove
        self.remove_mode = remove_mode
        self.reference_replaced_arguments = {}
        self.output = None

    @staticmethod
    def load_properties_with_default_values(properties, lookups):
        pointer_name = properties["pointer"]
        assert pointer_name in lookups, f"There is no pointer called {pointer_name} in {pformat(lookups)}"
        return {
            "pointer": lookups[pointer_name],
            "partial": properties.get("partial", False),
            "arguments": properties.get("arguments", {}),
            "output_names": properties.get("output_names", []),
            "should_remove": properties.get("should_remove", False),
            "remove_mode": properties.get("remove_mode", NodeRemoveMode.AUTO),
            "tags": properties.get("tags", []),
        }

    def __repr__(self):
        return dedent(
            f"""
            Name: {self.name}
            Pointer: {self.pointer}
            Arguments: {pformat(self.arguments)}
            Reference Replaced Arguments: {pformat(self.reference_replaced_arguments)}
            Should Remove: {self.should_remove}
            Remove Mode: {self.remove_mode}
            Tags: {self.tags},
        """
        )

    def create_output(self):
        assert not isinstance(self.output_names, str), f"The output_names for node: {self.name} can't be a string, only a list"
        self._call_pointer_and_set_output()

    def _call_pointer_and_set_output(self):
        if self.partial:
            assert (
                len(self.output_names) == 1
            ), f"If the output of node: {self.name} is partial, then there should be one output, {len(self.output_names)} outputs are found"
            self.output = {self.output_names[0]: functools.partial(self.pointer, **self.reference_replaced_arguments)}
        else:
            try:
                output = self.pointer(**self.reference_replaced_arguments)
            except TypeError as e:
                logger.error(e)
                logger.error(f"This error was produced when calling node:\n{self}")
                logger.error(e, exc_info=True)
                raise e

            if output is not None:
                assert len(self.output_names) > 0, f"There are no output_names defined in properties for the node: {self.name}"
                iterable_output = [output] if len(self.output_names) == 1 else output
                self.output = {output_name: output_value for output_name, output_value in zip(self.output_names, iterable_output)}


def remove_node_arguments(arguments, nodes_to_remove):
    if isinstance(arguments, dict):
        name_of_arguments_to_remove = []
        for name, value in arguments.items():
            updated_argument = remove_node_arguments(value, nodes_to_remove)
            if updated_argument == SHOULD_REMOVE_ARGUMENT:
                name_of_arguments_to_remove.append(name)
        for name in name_of_arguments_to_remove:
            del arguments[name]
    elif isinstance(arguments, list):
        values_to_remove = []
        for value in arguments:
            updated_argument = remove_node_arguments(value, nodes_to_remove)
            if updated_argument == SHOULD_REMOVE_ARGUMENT:
                values_to_remove.append(value)
        for value in values_to_remove:
            arguments.remove(value)
    elif isinstance(arguments, Reference):
        should_remove = arguments.ref_node_name in [node_to_remove.name for node_to_remove in nodes_to_remove]
        if should_remove:
            return SHOULD_REMOVE_ARGUMENT
    return arguments
