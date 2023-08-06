import inspect
from copy import deepcopy
from pprint import pformat

from ..logger import logger
from .yaml_loader import Reference


def flatten_resources_dict(d):
    flattened = dict()
    for k, v in d.items():
        assert (
            type(v) is not str
        ), f"The field: {v} is not a dictionary\nCheck if there is a field named 'properties' in the in your node containing fields:\n{pformat(d)}"

        if "properties" in v.keys():
            flattened.update(**{k: v})
        else:
            flattened.update(**flatten_resources_dict(v))
    return flattened


def find_references(resource):
    references = []
    if isinstance(resource, dict):
        for _, value in resource.items():
            references.extend(find_references(value))
    elif isinstance(resource, list):
        for value in resource:
            references.extend(find_references(value))
    elif isinstance(resource, Reference):
        references.append(resource)
    else:
        pass
    return references


def replace_arguments(pipeline, node):
    try:
        arguments = node.arguments
        needs_pipeline = "pipeline" in inspect.signature(node.pointer).parameters
        needs_config = "config" in inspect.signature(node.pointer).parameters
        needs_lookup = "lookup" in inspect.signature(node.pointer).parameters

        if arguments is not None:
            reference_replaced_arguments = replace_references(pipeline.graph, deepcopy(arguments))
            if needs_pipeline:
                reference_replaced_arguments["pipeline"] = pipeline
            if needs_config:
                reference_replaced_arguments["config"] = pipeline.config
            if needs_lookup:
                reference_replaced_arguments["lookup"] = pipeline.lookup

            return reference_replaced_arguments
    except AttributeError as e:
        logger.warning(e)
        return {}


def replace_should_remove(graph, node):
    return replace_references(graph, deepcopy(node.should_remove))


def replace_should_run(graph, node):
    return replace_references(graph, deepcopy(node.should_run))


def replace_references(graph, references):
    if isinstance(references, dict):
        for name, reference in references.items():
            references[name] = replace_references(graph, reference)
    elif isinstance(references, list):
        for i, reference in enumerate(references):
            references[i] = replace_references(graph, reference)
    elif isinstance(references, Reference):
        # reassign name it make the intent clearer
        reference = references
        ref_node = graph.nodes(data=True)[reference.ref_node_name]["node"]
        ref_node_outputs = ref_node.output
        assert ref_node_outputs is not None, f"Node: {reference.ref_node_name} has no output"
        assert reference.output_name in ref_node_outputs, f"Node: {reference.ref_node_name} has no output named {reference.output_name}"
        references = ref_node_outputs[reference.output_name]
    else:
        return references
    return references
