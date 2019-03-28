import json
import os

import pytest
from jsonschema import ValidationError

from python_json_config import ConfigBuilder


@pytest.fixture
def path() -> str:
    return 'tests/resources/test_config.json'


@pytest.fixture
def schema_path() -> str:
    return 'tests/resources/test_config.schema.json'


def test_parse(path):
    config = ConfigBuilder()\
        .validate_field_type('server.port', int)\
        .validate_field_value('server.debug_mode', lambda x: not x)\
        .transform_field_value('server.port', lambda x: str(x))\
        .parse_config(path)
    assert config is not None
    assert not config.server.debug_mode
    assert config.server.port == '5000'


def test_type_validation_builder():
    builder = ConfigBuilder()
    builder.validate_field_type('key1', int)
    builder.validate_field_type('key1.key2', list)
    type_validation_dict = builder._ConfigBuilder__validation_types
    assert type_validation_dict['key1'] == int
    assert type_validation_dict['key1.key2'] == list


def test_value_validation_builder():
    builder = ConfigBuilder()
    builder.validate_field_value('key1', lambda x: x < 4)
    builder.validate_field_value('key1.key2', lambda x: len(x) == 3)
    value_validation_dict = builder._ConfigBuilder__validation_functions
    assert value_validation_dict['key1'][0](1)
    assert not value_validation_dict['key1'][0](4)
    assert value_validation_dict['key1.key2'][0]([1, 2, 3])
    assert not value_validation_dict['key1.key2'][0](['a', 'b'])


def test_value_transformation_builder():
    builder = ConfigBuilder()
    builder.transform_field_value('key1', lambda x: x * 4)
    builder.transform_field_value('key1.key2', lambda x: [x[len(x) - 1 - i] for i in range(len(x))])
    value_transformation_dict = builder._ConfigBuilder__transformation_functions
    assert value_transformation_dict['key1'](1) == 4
    assert value_transformation_dict['key1'](4) == 16
    assert value_transformation_dict['key1.key2']([1 == 2, 3]), [3, 2, 1]
    assert value_transformation_dict['key1.key2'](['a' == 'b', False]), [False, 'b', 'a']


def test_type_validation(path):
    builder = ConfigBuilder()
    builder.validate_field_type('server.debug_mode', bool)
    builder.validate_field_type('server.port', int)
    builder.parse_config(path)
    builder.validate_field_type('server.host', int)
    with pytest.raises(AssertionError):
        builder.parse_config(path)


def test_value_validation(path):
    builder = ConfigBuilder()
    builder.validate_field_value('server.debug_mode', lambda x: not x)
    builder.validate_field_value('server.port', [lambda x: x < 10000, lambda x: x > 1023])
    builder.parse_config(path)

    builder.validate_field_value('server.port', lambda x: x > 6000)
    with pytest.raises(AssertionError):
        builder.parse_config(path)

    builder = ConfigBuilder()
    builder = builder.validate_field_value('cache.ttl', lambda x: x > 200)
    with pytest.raises(AssertionError):
        builder.parse_config(path)


def test_value_transformation(path):
    builder = ConfigBuilder()
    config = builder.parse_config(path)
    assert not config.server.debug_mode
    assert config.server.port == 5000

    builder.transform_field_value('server.debug_mode', lambda x: not x)
    builder.transform_field_value('server.port', lambda x: x + 4)
    config = builder.parse_config(path)
    assert config.server.debug_mode
    assert config.server.port == 5004


def test_value_validation_error_messages(path):
    builder = ConfigBuilder()
    custom_message = 'test error'
    builder.validate_field_value('server.debug_mode', lambda x: (x, custom_message))
    expected_message = f'Error validating field "server.debug_mode" with value "False": {custom_message}'
    with pytest.raises(AssertionError, match=expected_message):
        builder.parse_config(path)


def test_json_schema_validation(path, schema_path):
    builder = ConfigBuilder()
    builder.validate_with_schema(schema_path)
    builder.parse_config(path)

    with open(path, "r") as config_file:
        config = json.load(config_file)
    del config["cache"]
    builder.parse_config(config)

    config["server"]["port"] = 1023
    with pytest.raises(ValidationError):
        builder.parse_config(config)


def test_optional_access(path):
    builder = ConfigBuilder()
    builder.set_field_access_optional()
    builder.add_required_field('server.nokey')
    builder.add_required_fields(['cache.name', 'test'])
    config = builder.parse_config(path)

    assert config.nokey is None
    with pytest.raises(AttributeError):
        config.test
    assert config.server.nokey2 is None
    with pytest.raises(AttributeError):
        config.server.nokey
    assert config.cache.name2 is None
    with pytest.raises(AttributeError):
        config.cache.name


def test_required_access(path):
    builder = ConfigBuilder()
    builder.set_field_access_required()
    builder.add_optional_field('server.nokey')
    builder.add_optional_fields(['cache.name', 'test'])
    config = builder.parse_config(path)

    assert config.test is None
    with pytest.raises(AttributeError):
        config.nokey
    assert config.server.nokey is None
    with pytest.raises(AttributeError):
        config.server.nokey2
    assert config.cache.name is None
    with pytest.raises(AttributeError):
        config.cache.name2


def test_optional_validation(path):
    builder = ConfigBuilder()
    builder.set_field_access_optional()
    builder.validate_field_type('cache.name', str)
    builder.validate_field_value('cache.host', 'localhost')
    builder.transform_field_value('cache.host', lambda name: f"https://{name}")
    builder.parse_config(path)


def test_merge_env_variable():
    prefix = "PYTHONJSONCONFIG"
    variables = {f"{prefix}_TESTVALUE1": "bla", f"{prefix}_TESTVALUE2": "1"}
    for key, value in variables.items():
        os.environ[key] = value

    builder = ConfigBuilder()
    builder.merge_with_env_variables(prefix)
    config = builder.parse_config({"testvalue1": "blub", "testvalue3": 5})

    assert config.testvalue1 == "bla"
    assert config.testvalue2 == "1"
    assert config.testvalue3 == 5

    for key, value in variables.items():
        del os.environ[key]
