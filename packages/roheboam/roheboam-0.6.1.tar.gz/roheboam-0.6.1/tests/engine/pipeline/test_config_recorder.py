from roheboam.engine.pipeline import (
    ConfigurationNodeRecorder,
    Pipeline,
    Reference,
    Variable,
    create_output_names,
)


def test_create_output_names():
    def f1():
        return 1, 2

    def f2():
        return [1, 2]

    def f3():
        return [1, 2], 2

    f1_return_names = create_output_names(f1)
    assert f1_return_names == ["0", "1"]

    f2_return_names = create_output_names(f2)
    assert f2_return_names == ["0"]

    f3_return_names = create_output_names(f3)
    assert f3_return_names == ["0", "1"]


def test_configuration_node_recorder_record_with_single_node():
    def f1(x):
        return x + 1

    cfg_node_recorder = ConfigurationNodeRecorder()
    cfg_node_recorder.reset_recorded_nodes()
    f1 = cfg_node_recorder.record(f1)
    f1_output = f1(1)
    assert f1_output == 2
    assert f1_output.node_name == "f1_0"
    assert f1_output.output_name == "0"
    assert f1.variables == {Variable(variable_group="f1_0", variable_name="x"): 1}, f"config_f1.variables is {f1.variables}"
    assert f1.config_properties == {
        "properties": {
            "arguments": {
                "x": Variable(variable_group="f1_0", variable_name="x"),
            },
            "output_names": ["0"],
            "pointer": "f1",
            "tags": [],
        }
    }


def test_configuration_node_recorder_record_with_single_node_with_tag():
    def f1(x):
        return x + 1

    cfg_node_recorder = ConfigurationNodeRecorder()
    cfg_node_recorder.reset_recorded_nodes()
    f1 = cfg_node_recorder.record(f1, tags=["TRAIN"])
    f1_output = f1(1)
    assert f1_output == 2
    assert f1_output.node_name == "f1_0"
    assert f1_output.output_name == "0"
    assert f1.variables == {Variable(variable_group="f1_0", variable_name="x"): 1}, f"config_f1.variables is {f1.variables}"
    assert f1.config_properties == {
        "properties": {
            "arguments": {
                "x": Variable(variable_group="f1_0", variable_name="x"),
            },
            "output_names": ["0"],
            "pointer": "f1",
            "tags": ["TRAIN"],
        }
    }


def test_configuration_node_recorder_record_with_multiple_nodes():
    def f1(x):
        return x + 1

    def f2(y):
        return y + 2

    cfg_node_recorder = ConfigurationNodeRecorder()
    cfg_node_recorder.reset_recorded_nodes()
    f1 = cfg_node_recorder.record(f1)
    f1_output = f1(1)
    assert f1_output == 2
    assert f1_output.node_name == "f1_0"
    assert f1_output.output_name == "0"
    assert f1.variables == {Variable(variable_group="f1_0", variable_name="x"): 1}, f"config_f1.variables is {f1.variables}"
    assert f1.arguments == {"x": Variable(variable_group="f1_0", variable_name="x")}
    assert f1.config_properties == {
        "properties": {"arguments": {"x": Variable(variable_group="f1_0", variable_name="x")}, "output_names": ["0"], "pointer": "f1", "tags": []}
    }

    recorded_f2 = cfg_node_recorder.record(f2)
    f2_output = recorded_f2(f1_output)
    assert f2_output == 4
    assert f2_output.node_name == "f2_0"
    assert f2_output.output_name == "0"
    assert recorded_f2.variables == {}, f"config_f2.variables is {f2.variables}"
    assert recorded_f2.arguments == {"y": Reference(ref_node_name="f1_0", output_name="0")}
    assert recorded_f2.config_properties == {
        "properties": {"arguments": {"y": Reference(ref_node_name="f1_0", output_name="0")}, "output_names": ["0"], "pointer": "f2", "tags": []}
    }


def test_configuration_node_recorder_build_with_single_node():
    def f1(x):
        return x + 1

    cfg_node_recorder = ConfigurationNodeRecorder()
    cfg_node_recorder.reset_recorded_nodes()
    recorded_f1 = cfg_node_recorder.record(f1)
    assert recorded_f1(1) == 2
    assert cfg_node_recorder.config == {
        "Variables": {
            "f1_0": {"x": 1},
        },
        "Resources": {
            "f1_0": {
                "properties": {
                    "pointer": "f1",
                    "arguments": {"x": Variable(variable_group="f1_0", variable_name="x")},
                    "output_names": ["0"],
                    "tags": [],
                }
            }
        },
    }
    assert cfg_node_recorder.lookup == {"f1": f1}


def test_configuration_node_recorder_build_with_multiple_nodes():
    def f1(x):
        return x + 1

    def f2(y):
        return y + 2

    cfg_node_recorder = ConfigurationNodeRecorder()
    cfg_node_recorder.reset_recorded_nodes()
    recorded_f1 = cfg_node_recorder.record(f1)
    recorded_f2 = cfg_node_recorder.record(f2)

    assert recorded_f1(1) == 2
    assert recorded_f2(recorded_f1(1)) == 4
    assert cfg_node_recorder.config == {
        "Variables": {"f1_0": {"x": 1}},
        "Resources": {
            "f1_0": {
                "properties": {
                    "pointer": "f1",
                    "arguments": {"x": Variable(variable_group="f1_0", variable_name="x")},
                    "output_names": ["0"],
                    "tags": [],
                }
            },
            "f2_0": {
                "properties": {
                    "pointer": "f2",
                    "arguments": {"y": Reference(ref_node_name="f1_0", output_name="0")},
                    "output_names": ["0"],
                    "tags": [],
                }
            },
        },
    }
    assert cfg_node_recorder.lookup == {
        "f1": f1,
        "f2": f2,
    }


def test_integration_with_pipeline():
    def add_one(x):
        return x + 1

    cfg_node_recorder = ConfigurationNodeRecorder()

    add_one_recorded = cfg_node_recorder.record(add_one)
    add_one_output = add_one_recorded(2)
    assert add_one_output == 3

    config = cfg_node_recorder.config
    lookup = cfg_node_recorder.lookup

    pipeline = Pipeline.create_from_config(config, lookup)

    pipeline.run()

    assert pipeline.get_node_output("add_one_0") == 3
