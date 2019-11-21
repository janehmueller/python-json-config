from python_json_config.utils import parse_env_variable_name


def test_underscore_splitting():
    variable = "test__key_subkey"
    split = parse_env_variable_name(variable)
    assert split == ["test_key", "subkey"]
