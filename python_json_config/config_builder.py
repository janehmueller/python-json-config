import json
from typing import Dict, Union, List

import jsonschema

from .config_node import Config


class ConfigBuilder(object):
    def __init__(self):
        self.__config: Config = None

        # custom validation and transformation settings
        self.__validation_types: Dict[str, type] = {}
        self.__validation_functions: Dict[str, list] = {}
        self.__transformation_functions = {}

        # stores the json schema used to validate the config
        self.__json_schema: dict = None

        # settings of required and optional fields and (non-)strict access
        self.__strict_access: bool = None
        self.__field_access_settings: Dict[str, bool] = {}

    def validate_field_type(self, field_name: str, field_type: type):
        self.__validation_types[field_name] = field_type
        return self

    def __validate_types(self):
        for field_name, field_type in self.__validation_types.items():
            value = self.__config.get(field_name)
            assert isinstance(value, field_type), f'Config field "{field_name}" with value "{value}" is not of type {field_type}'

    def validate_field_value(self, field_name: str, validation_function):
        if field_name not in self.__validation_functions:
            self.__validation_functions[field_name] = []

        if isinstance(validation_function, list):
            self.__validation_functions[field_name] += validation_function
        else:
            self.__validation_functions[field_name].append(validation_function)

        return self

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

    def transform_field_value(self, field_name: str, transformation_function):
        self.__transformation_functions[field_name] = transformation_function
        return self

    def __transform_field_values(self):
        for field_name, transformation_function in self.__transformation_functions.items():
            value = self.__config.get(field_name)
            new_value = transformation_function(value)
            self.__config.update(field_name, new_value)

    def validate_with_schema(self, schema: Union[str, dict]):
        """
        Save the jsonschema for later validation.
        :param schema: The jsonschema with which the config will be validated. Can be either a file path to a JSON file
                       containing the schema or an already parsed dictionary.
        """
        if isinstance(schema, dict):
            self.__json_schema = schema
        else:
            with open(schema, "r") as json_file:
                self.__json_schema = json.load(json_file)

    def set_field_access_optional(self):
        self.__strict_access = False

    def set_field_access_required(self):
        self.__strict_access = True

    def add_required_field(self, field_name: str):
        self.__field_access_settings[field_name] = True

    def add_required_fields(self, field_names: List[str]):
        for field in field_names:
            self.add_required_field(field)

    def add_optional_field(self, field_name: str):
        self.__field_access_settings[field_name] = False

    def add_optional_fields(self, field_names: List[str]):
        for field in field_names:
            self.add_optional_field(field)

    def parse_config(self, config: Union[str, dict]) -> Config:
        if isinstance(config, dict):
            config_dict = config
        else:
            with open(config, "r") as json_file:
                config_dict = json.load(json_file)

        if self.__json_schema is not None:
            jsonschema.validate(config_dict, self.__json_schema)
        self.__config = Config(config_dict,
                               strict_access=self.__strict_access,
                               required_fields=[field for field, status in self.__field_access_settings.items() if status],
                               optional_fields=[field for field, status in self.__field_access_settings.items() if not status])
        self.__validate_types()
        self.__validate_field_values()
        self.__transform_field_values()

        return self.__config




