import json
from typing import Dict, Union

import jsonschema

from .config_node import Config


class ConfigBuilder(object):
    def __init__(self):
        self.__validation_types: Dict[str, type] = {}
        self.__validation_functions: Dict[str, list] = {}
        self.__transformation_functions = {}
        self.__config: Config = None
        self.__json_schema: dict = None

    def validate_field_type(self, field_name: str, field_type: type):
        self.__validation_types[field_name] = field_type
        return self

    def validate_field_value(self, field_name: str, validation_function):
        if field_name not in self.__validation_functions:
            self.__validation_functions[field_name] = []

        if isinstance(validation_function, list):
            self.__validation_functions[field_name] += validation_function
        else:
            self.__validation_functions[field_name].append(validation_function)

        return self

    def transform_field_value(self, field_name: str, transformation_function):
        self.__transformation_functions[field_name] = transformation_function
        return self

    def validate_with_schema(self, schema: Union[str, dict]):
        if isinstance(schema, dict):
            self.__json_schema = schema
        else:
            with open(schema, "r") as json_file:
                self.__json_schema = json.load(json_file)

    def parse_config(self, config: Union[str, dict]) -> Config:
        if isinstance(config, dict):
            config_dict = config
        else:
            with open(config, "r") as json_file:
                config_dict = json.load(json_file)

        if self.__json_schema is not None:
            jsonschema.validate(config_dict, self.__json_schema)
        self.__config = Config(config_dict)
        self.__validate_types()
        self.__validate_field_values()
        self.__transform_field_values()

        return self.__config

    def __validate_types(self):
        for field_name, field_type in self.__validation_types.items():
            value = self.__config.get(field_name)
            assert isinstance(value, field_type), f'Config field "{field_name}" with value "{value}" is not of type {field_type}'

    def __validate_field_values(self):
        for field_name, validation_functions in self.__validation_functions.items():
            value = self.__config.get(field_name)
            for validation_function in validation_functions:
                validation_result = validation_function(value)
                error_message = f'Error validating field "{field_name}" with value "{value}"'

                if isinstance(validation_result, tuple):
                    result, validation_error = validation_result
                    assert result, f"{error_message}: {validation_error}"
                else:
                    assert validation_result, error_message

    def __transform_field_values(self):
        for field_name, transformation_function in self.__transformation_functions.items():
            value = self.__config.get(field_name)
            new_value = transformation_function(value)
            self.__config.update(field_name, new_value)
