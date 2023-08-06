from roheboam.engine.pipeline import Reference, Variable, load_config_from_string, merge_dicts


def test_load_reference():
    document = """
    Resources:
      ResourceBar:
        arg1: !Ref Foo.Bar
    """

    config = load_config_from_string(document, with_variable_replacement=False)
    assert config == {"Resources": {"ResourceBar": {"arg1": Reference(ref_node_name="Foo", output_name="Bar")}}}


def test_load_variable():
    document = """
    Variables:
      ResourceBarVar:
        Bar: bar
    Resources:
      ResourceBar:
        arg1: !Var ResourceBarVar.Bar
    """

    config = load_config_from_string(document, with_variable_replacement=False)
    assert config == {
        "Variables": {"ResourceBarVar": {"Bar": "bar"}},
        "Resources": {"ResourceBar": {"arg1": Variable(variable_group="ResourceBarVar", variable_name="Bar")}},
    }


def test_variable_replacement():
    document = """
    Variables:
      single_variable: hello
    Resources:
      TestVariableReplacement:
        single_variable: !Var single_variable
    """

    config = load_config_from_string(document, with_variable_replacement=True)

    assert config == {"Resources": {"TestVariableReplacement": {"single_variable": "hello"}}, "Variables": {"single_variable": "hello"}}


def test_variable_in_group_replacement():
    document = """
    Variables:
      TestVariableInGroupReplacement:
        single_variable: hello
    Resources:
      TestVariableInGroupReplacement:
        single_variable: !Var TestVariableInGroupReplacement.single_variable
    """

    config = load_config_from_string(document, with_variable_replacement=True)

    assert config == {
        "Variables": {"TestVariableInGroupReplacement": {"single_variable": "hello"}},
        "Resources": {"TestVariableInGroupReplacement": {"single_variable": "hello"}},
    }


def test_variables_in_list_replacement():
    document = """
    Variables:
      variable_one: hello
      variable_two: bye
    Resources:
      TestVariableInListReplacement:
        - !Var variable_one
        - !Var variable_two
    """
    config = load_config_from_string(document, with_variable_replacement=True)
    assert config == {
        "Variables": {"variable_one": "hello", "variable_two": "bye"},
        "Resources": {"TestVariableInListReplacement": ["hello", "bye"]},
    }


def test_variable_in_list_of_dict_replacement():
    document = """
    Variables:
      variable_one: hello
    Resources:
      TestVariableInListOfDictReplacement:
        - key1: !Var variable_one
    """
    config = load_config_from_string(document, with_variable_replacement=True)
    assert config == {"Variables": {"variable_one": "hello"}, "Resources": {"TestVariableInListOfDictReplacement": [{"key1": "hello"}]}}


def test_variable_in_list_of_nested_dict_replacement():
    document = """
    Variables:
      variable_one: hello
    Resources:
      TestVariableInListOfNestedDictReplacement:
        - key1:
            key2: !Var variable_one
    """
    config = load_config_from_string(document, with_variable_replacement=True)
    assert config == {
        "Variables": {"variable_one": "hello"},
        "Resources": {"TestVariableInListOfNestedDictReplacement": [{"key1": {"key2": "hello"}}]},
    }


def test_nested_variable_replacement():
    document = """
      Variables:
          VariableGroup:
              VariableSubGroup:
                variable_one: hello
      Resources:
        TestVariableInListOfNestedDictReplacement:
          - key1:
              key2: !Var VariableGroup.VariableSubGroup.variable_one
    """
    config = load_config_from_string(document, with_variable_replacement=True)
    assert config == {
        "Variables": {"VariableGroup": {"VariableSubGroup": {"variable_one": "hello"}}},
        "Resources": {"TestVariableInListOfNestedDictReplacement": [{"key1": {"key2": "hello"}}]},
    }


def test_merge_three_dicts():
    A = {"Variables": {"V1": {"A": "A"}, "V2": {"A": {"B": "B"}}}, "Resources": {"R1": {"A": "A"}}}

    B = {"Variables": {"V1": {"B": "B", "C": "C"}, "V2": {"A": {"C": "C"}, "B": "B"}}, "Resources": {"R1": {"B": "B"}}}

    C = {"Resources": {"R2": {"A": "A"}}, "Variables": {"V1": {"D": "D"}}}

    assert merge_dicts([A, B, C]) == {
        "Variables": {"V1": {"A": "A", "B": "B", "C": "C", "D": "D"}, "V2": {"A": {"B": "B", "C": "C"}, "B": "B"}},
        "Resources": {"R1": {"A": "A", "B": "B"}, "R2": {"A": "A"}},
    }


def test_merge_two_dicts():
    A = {"Variables": {"V1": {"A": "A"}, "V2": {"A": {"B": "B"}}}, "Resources": {"R1": {"A": "A"}}}

    B = {"Variables": {"V1": {"B": "B", "C": "C"}, "V2": {"A": {"C": "C"}, "B": "B"}}, "Resources": {"R1": {"B": "B"}}}

    merge_dicts([A, B]) == {
        "Variables": {"V1": {"A": "A", "B": "B", "C": "C"}, "V2": {"A": {"B": "B", "C": "C"}, "B": "B"}},
        "Resources": {"R1": {"A": "A", "B": "B"}},
    }
