import networkx as nx

from roheboam.engine.pipeline import (
    Node,
    NodeRemoveMode,
    Pipeline,
    Reference,
    remove_node_arguments,
)


def test_pipeline_nodes_to_be_removed_with_boolean():
    pointer_a = lambda: 1
    node_a = Node(name="A", references=[], pointer=pointer_a, partial=False, arguments={}, output_names=["output_1"], should_remove=True)
    graph = nx.DiGraph()
    graph.add_node("A", node=node_a)

    pipeline = Pipeline.create_from_graph_with_no_config_and_lookup(graph)
    nodes_to_be_removed = pipeline._nodes_to_be_removed()

    assert len(nodes_to_be_removed) == 1
    assert nodes_to_be_removed == [node_a]


def test_pipeline_nodes_to_be_removed_with_reference():
    pointer_a = lambda: 1
    pointer_b = lambda x: x + 1
    node_a = Node(name="A", references=[], pointer=pointer_a, partial=False, arguments={}, output_names=["output_1"], should_remove=True)
    node_b = Node(
        name="B",
        references=[Reference(ref_node_name="A", output_name="output_1")],
        pointer=pointer_b,
        partial=False,
        arguments={"x": Reference(ref_node_name="A", output_name="output_1")},
        output_names=["output_1"],
    )
    graph = nx.DiGraph()
    graph.add_node("A", node=node_a)
    graph.add_node("B", node=node_b)
    pipeline = Pipeline.create_from_graph_with_no_config_and_lookup(graph)
    nodes_to_be_removed = pipeline._nodes_to_be_removed()
    assert len(nodes_to_be_removed) == 1
    assert nodes_to_be_removed == [node_a]


def test_pipeline_nodes_to_be_removed_should_not_remove_nodes_if_no_tags_passed():
    pointer_a = lambda: 1
    node_a = Node(name="A", references=[], pointer=pointer_a, partial=False, arguments={}, output_names=["output_1"])
    graph = nx.DiGraph()
    graph.add_node("A", node=node_a)

    pipeline = Pipeline.create_from_graph_with_no_config_and_lookup(graph)
    nodes_to_be_removed = pipeline._nodes_to_be_removed(tags_to_be_removed=[])

    assert len(nodes_to_be_removed) == 0
    assert nodes_to_be_removed == []


def test_pipeline_nodes_to_be_removed_should_not_remove_nodes_if_tags_passed():
    pointer_a = lambda: 1
    node_a = Node(name="A", references=[], pointer=pointer_a, partial=False, arguments={}, output_names=["output_1"], tags=["REMOVE_TAG"])
    graph = nx.DiGraph()
    graph.add_node("A", node=node_a)

    pipeline = Pipeline.create_from_graph_with_no_config_and_lookup(graph)
    nodes_to_be_removed = pipeline._nodes_to_be_removed(tags_to_be_removed=["REMOVE_TAG"])

    assert len(nodes_to_be_removed) == 1
    assert nodes_to_be_removed == [node_a]


def test_pipeline_run_for_node_to_be_removed_for_if_node_has_tag_in_remove_nodes_with_tags():
    pointer_a = lambda: 1
    node_a = Node(name="A", references=[], pointer=pointer_a, partial=False, arguments={}, output_names=["output_1"], tags=["REMOVE_TAG"])
    graph = nx.DiGraph()
    graph.add_node("A", node=node_a)

    pipeline = Pipeline.create_from_graph_with_no_config_and_lookup(graph)
    pipeline.run(remove_nodes_with_tags=["REMOVE_TAG"])

    node_a_reference_in_pipeline = pipeline.get_node("A")
    assert node_a_reference_in_pipeline.should_remove == True


def test_pipeline_run_remove_mode_propagate():
    pointer_b = lambda x: x + 1
    node_b = Node(
        name="B",
        references=[Reference(ref_node_name="A", output_name="output_1")],
        pointer=pointer_b,
        partial=False,
        arguments={"x": Reference(ref_node_name="A", output_name="output_1")},
        output_names=["output_1"],
    )
    pointer_a = lambda: 1
    node_a = Node(
        name="A",
        references=[],
        pointer=pointer_a,
        partial=False,
        arguments={},
        output_names=["output_1"],
        should_remove=True,
        remove_mode=NodeRemoveMode.PROPAGATE,
    )
    node_a.referenced_by = [node_b]

    graph = nx.DiGraph()
    graph.add_node("A", node=node_a)
    graph.add_node("B", node=node_b)
    pipeline = Pipeline.create_from_graph_with_no_config_and_lookup(graph)
    pipeline.run()

    assert node_a.should_remove is True
    assert node_b.should_remove is True


def test_pipeline_run_remove_mode_only():
    pointer_b = lambda x: [i for i in x]
    node_b = Node(
        name="B",
        references=[Reference(ref_node_name="A", output_name="output_1")],
        pointer=pointer_b,
        partial=False,
        arguments={"x": [Reference(ref_node_name="A", output_name="output_1")]},
        output_names=["output_1"],
    )
    pointer_a = lambda: 1
    node_a = Node(
        name="A",
        references=[],
        pointer=pointer_a,
        partial=False,
        arguments={},
        output_names=["output_1"],
        should_remove=True,
        remove_mode=NodeRemoveMode.ONLY,
    )
    node_a.referenced_by = [node_b]

    graph = nx.DiGraph()
    graph.add_node("A", node=node_a)
    graph.add_node("B", node=node_b)
    pipeline = Pipeline.create_from_graph_with_no_config_and_lookup(graph)
    pipeline.run()

    assert node_a.should_remove is True
    assert node_b.should_remove is False


def test_pipeline_run_remove_mode_auto_for_no_direct_reference():
    pointer_b = lambda x: [i for i in x]
    node_b = Node(
        name="B",
        references=[Reference(ref_node_name="A", output_name="output_1")],
        pointer=pointer_b,
        partial=False,
        arguments={"x": [Reference(ref_node_name="A", output_name="output_1")]},
        output_names=["output_1"],
    )
    pointer_a = lambda: 1
    node_a = Node(
        name="A",
        references=[],
        pointer=pointer_a,
        partial=False,
        arguments={},
        output_names=["output_1"],
        should_remove=True,
        remove_mode=NodeRemoveMode.AUTO,
    )
    node_a.referenced_by = [node_b]

    graph = nx.DiGraph()
    graph.add_node("A", node=node_a)
    graph.add_node("B", node=node_b)
    pipeline = Pipeline.create_from_graph_with_no_config_and_lookup(graph)
    pipeline.run()

    assert node_a.should_remove is True
    assert node_b.should_remove is False


def test_pipeline_run_remove_mode_auto_for_direct_reference():
    pointer_b = lambda x: x
    node_b = Node(
        name="B",
        references=[Reference(ref_node_name="A", output_name="output_1")],
        pointer=pointer_b,
        partial=False,
        arguments={"x": Reference(ref_node_name="A", output_name="output_1")},
        output_names=["output_1"],
    )
    pointer_a = lambda: 1
    node_a = Node(
        name="A",
        references=[],
        pointer=pointer_a,
        partial=False,
        arguments={},
        output_names=["output_1"],
        should_remove=True,
        remove_mode=NodeRemoveMode.AUTO,
    )
    node_a.referenced_by = [node_b]

    graph = nx.DiGraph()
    graph.add_node("A", node=node_a)
    graph.add_node("B", node=node_b)
    pipeline = Pipeline.create_from_graph_with_no_config_and_lookup(graph)
    pipeline.run()

    assert node_a.should_remove is True
    assert node_b.should_remove is True


def test_remove_node_arguments():
    pointer_a = lambda: 1
    pointer_b = lambda x: x + 1
    node_a = Node(name="A", references=[], pointer=pointer_a, partial=False, arguments={}, output_names=["output_1"], should_remove=True)
    node_b = Node(
        name="B",
        references=[Reference(ref_node_name="A", output_name="output_1")],
        pointer=pointer_b,
        partial=False,
        arguments={"x": Reference(ref_node_name="A", output_name="output_1")},
        output_names=["output_1"],
    )

    assert node_b.arguments == {"x": Reference(ref_node_name="A", output_name="output_1")}
    node_b_arguments_after_remove_node_arguments = remove_node_arguments(node_b.arguments, [node_a])
    assert node_b_arguments_after_remove_node_arguments == {}
