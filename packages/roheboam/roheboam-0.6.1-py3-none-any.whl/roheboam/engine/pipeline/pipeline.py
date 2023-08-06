import traceback
from copy import deepcopy

import networkx as nx

from ..logger import logger
from .config import Configuration
from .config_loader import (
    dump_config_to_string,
    load_config_from_path,
    load_config_from_paths,
    load_config_from_string,
    load_config_from_strings,
    replace_config_variables,
)
from .constants import RESOURCE_KEY
from .graph_construction import Reference, find_references, flatten_resources_dict, replace_arguments, replace_should_remove
from .node import Node, NodeRemoveMode, remove_node_arguments


class Pipeline:
    def __init__(self, graph, config, lookup):
        self.graph = graph
        self.config = config
        self.lookup = lookup

    @classmethod
    def create_from_graph_with_no_config_and_lookup(cls, graph):
        graph = cls._add_edges_to_graph(graph)
        return cls(graph, None, None)

    @classmethod
    def create_from_config(cls, config, lookup):
        assert config.get(RESOURCE_KEY) is not None, f"There is no {RESOURCE_KEY} key in the configuration file"

        raw_config = load_config_from_string(dump_config_to_string(config))

        config = Configuration(deepcopy(raw_config))

        variable_replaced_config = replace_config_variables(deepcopy(raw_config))
        flattened_resources = flatten_resources_dict(variable_replaced_config[RESOURCE_KEY])

        graph = nx.DiGraph()
        graph = cls._add_nodes_to_graph(graph, flattened_resources, lookup)
        graph = cls._add_edges_to_graph(graph)
        return cls(graph, config, lookup)

    @classmethod
    def create_from_config_string(cls, config_string, lookup, with_variable_replacement=False):
        config = load_config_from_string(config_string, with_variable_replacement=with_variable_replacement)
        return cls.create_from_config(config, lookup)

    @classmethod
    def create_from_config_strings(cls, config_strings, lookup, with_variable_replacement=False):
        config = load_config_from_strings(config_strings, with_variable_replacement=with_variable_replacement)
        return cls.create_from_config(config, lookup)

    @classmethod
    def create_from_config_path(cls, config_path, lookup, with_variable_replacement=False):
        config = load_config_from_path(config_path, with_variable_replacement=with_variable_replacement)
        return cls.create_from_config(config, lookup)

    @classmethod
    def create_from_config_paths(cls, config_paths, lookup, with_variable_replacement=False):
        config = load_config_from_paths(config_paths, with_variable_replacement=with_variable_replacement)
        return cls.create_from_config(config, lookup)

    @staticmethod
    def _add_nodes_to_graph(graph, resources, lookup):
        logger.info("Adding nodes to graph")
        for name, resource in resources.items():
            assert "properties" in resource, f"The properties key isn't defined for node: {name}"
            references = find_references(resource)
            properties = Node.load_properties_with_default_values(resource["properties"], lookup)
            node = Node(name=name, references=references, **properties)
            graph.add_node(name, node=node)
        return graph

    @staticmethod
    def _add_edges_to_graph(graph):
        logger.info("Adding edges to graph")
        for name, node_wrapper in graph.nodes(data=True):
            node = node_wrapper["node"]
            for reference in node.references:
                referenced_node_name = reference.ref_node_name

                assert (
                    referenced_node_name in graph.nodes
                ), f"The reference {referenced_node_name} in node {node.name} does not exist, \
                    try checking if {referenced_node_name} is defined in the configuration"

                referenced_node = graph.nodes(data=True)[referenced_node_name]["node"]
                referenced_node.referenced_by.append(node)

                graph.add_edge(referenced_node_name, name)
        return graph

    @property
    def variables(self):
        return self.config.variables

    @property
    def sorted_node_names(self):
        return list(nx.algorithms.dag.topological_sort(self.graph))

    def get_node(self, name):
        return self.graph.nodes(data=True)[name]["node"]

    def get_node_output_lookup(self, name):
        return self.get_node(name).output

    def get_node_output(self, name, output_lookup_key=None):
        output_lookup = self.get_node_output_lookup(name)
        if output_lookup is None:
            return None

        if output_lookup_key is None and len(output_lookup) == 1:
            output = list(output_lookup.values())[0]
            return output
        else:
            return output_lookup[output_lookup_key]

    def node_exists(self, name):
        return name in self.graph.nodes()

    def _nodes_to_be_removed(self, tags_to_be_removed=[]):
        nodes_to_be_removed = []
        for node_name in self.graph:
            node = self.graph.nodes(data=True)[node_name]["node"]
            node_tag_is_in_tags_to_be_removed = len(set(node.tags) & set(tags_to_be_removed)) > 0
            if node.should_remove or node_tag_is_in_tags_to_be_removed:
                nodes_to_be_removed.append(node)
        return nodes_to_be_removed

    def run(self, to_node=None, remove_nodes_with_tags=[]):
        has_error = False
        errors = []
        for node_name in nx.algorithms.dag.topological_sort(self.graph):
            try:
                node = self.graph.nodes(data=True)[node_name]["node"]

                # Replace all `References` of a removed node in the arguments
                # of the current `node` to SHOULD_REMOVE_ARGUMENT.
                # This is needed # as nodes that are removed from the graph won't
                # be run, as a result there will be no output and references to a
                # node's output for a node that hasn't been run will fail
                self._update_node_arguments_for_removed_nodes(node, self._nodes_to_be_removed(remove_nodes_with_tags))

                # replace all references in the argument of the current `node`
                self._update_node_arguments_references(node)

                # update `node.should_run` & replace the reference if it exists
                # self._update_node_should_run(node)

                # update `node.should_remove` & replace the reference if it exists
                self._update_node_should_remove(node, remove_nodes_with_tags)

                logger.info(f"Processing node: {node_name} | Should run: {not node.should_remove}")

                if not node.should_remove:
                    logger.debug(f"Running node: {node.name}")
                    node.create_output()

                if to_node == node_name:
                    break

            except Exception:
                has_error = True
                error = "\n".join(
                    [
                        f"An error has happened when trying to run node: {node_name}",
                        f"The state when the node failed is: {node}",
                        f"{traceback.format_exc()}",
                        "\n",
                    ]
                )
                errors.append(error)

        if has_error:
            raise ValueError(f"There were errors while running the graph:\n\n{(''.join(errors))}")

    def _update_node_arguments_for_removed_nodes(self, node, nodes_to_be_removed):
        logger.debug(f"Updating node arguments for removed nodes: {node.name}")
        node.arguments = remove_node_arguments(node.arguments, nodes_to_be_removed)

    def _update_node_arguments_references(self, node):
        logger.debug(f"Replacing references for node: {node.name}")
        logger.debug(f"Original arguments: {node.arguments}")
        reference_replaced_arguments = replace_arguments(self, node)
        node.reference_replaced_arguments.update(**reference_replaced_arguments)
        logger.debug(f"Replaced arguments: {node.reference_replaced_arguments}")

    def _update_node_should_remove(self, node, tags_to_be_removed):
        logger.debug(f"Updating should_remove property for node: {node.name}")

        # case for NodeRemoveMode.ONLY
        node_should_remove = self._get_node_should_remove(node, tags_to_be_removed)
        node.should_remove = node_should_remove

        if node.remove_mode == NodeRemoveMode.PROPAGATE:
            for referenced_node in node.referenced_by:
                if isinstance(referenced_node.should_remove, Reference) or referenced_node.should_remove is True:
                    continue
                else:
                    referenced_node.should_remove = node_should_remove
                    self._update_node_should_remove(referenced_node, tags_to_be_removed)

        elif node.remove_mode == NodeRemoveMode.AUTO:
            for referenced_node in node.referenced_by:
                if isinstance(referenced_node.should_remove, Reference) or referenced_node.should_remove is True:
                    continue
                else:
                    for arg_name, arg_value in referenced_node.arguments.items():
                        # if the reference node uses the current node & there is no default argument for it, then propagate
                        if isinstance(arg_value, Reference) and arg_value.ref_node_name == node.name:
                            logger.debug(f"Remove argument '{arg_name}' with value '{arg_value}' for node {node.name}: True")
                            referenced_node.should_remove = node_should_remove
                            self._update_node_should_remove(referenced_node, tags_to_be_removed)
                        else:
                            logger.debug(f"Remove argument '{arg_name}' with value '{arg_value}' for node {node.name}: False")

    def _get_node_should_remove(self, node, tags_to_be_removed):
        if isinstance(node.should_remove, Reference):
            node_should_remove_property = replace_should_remove(self.graph, node)
        else:
            node_should_remove_property = node.should_remove
        node_tag_is_in_tags_to_be_removed = len(set(node.tags) & set(tags_to_be_removed)) > 0
        return node_should_remove_property or node_tag_is_in_tags_to_be_removed

    def _run_node(self, node):
        node.create_output()
