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
        """
        Validate that the given field is of the given type when the final config is built.
        :param field_name: The field that is validated.
        :param field_type: The type that the field value should have.
        :return: The builder object for chaining of calls.
        """
        self.__validation_types[field_name] = field_type
        return self

    def __validate_types(self):
        for field_name, field_type in self.__validation_types.items():
            value = self.__config.get(field_name)
            # skip optional fields that do not exist
            if value is None:
                continue
            assert isinstance(value, field_type), f'Config field "{field_name}" with value "{value}" is not of ' \
                f'type {field_type}'

    def validate_field_value(self, field_name: str, validation_function):
        """
        Validate that the validation function returns true with the value of the given field when the final config is
        built.
        :param field_name: The field that is validated.
        :param validation_function: Function that takes the field value as input and validates it (returns True if the
                                    value is valid and False if it is invalid).
        :return: The builder object for chaining of calls.
        """
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
            # skip optional fields that do not exist
            if value is None:
                continue
            for validation_function in validation_functions:
                validation_result = validation_function(value)
                error_message = f'Error validating field "{field_name}" with value "{value}"'

                if isinstance(validation_result, tuple):
                    result, validation_error = validation_result
                    assert result, f"{error_message}: {validation_error}"
                else:
                    assert validation_result, error_message

    def transform_field_value(self, field_name: str, transformation_function):
        """
        Transform the given field value with the transformation function when the final config is built.
        The transformation function takes the field value as input and returns a new value.
        :param field_name: The field that is validated.
        :param transformation_function: Function that takes the field value as input and transforms it into another
                                        value.
        :return: The builder object for chaining of calls.
        """
        self.__transformation_functions[field_name] = transformation_function
        return self

    def __transform_field_values(self):
        for field_name, transformation_function in self.__transformation_functions.items():
            value = self.__config.get(field_name)
            # skip optional fields that do not exist
            if value is None:
                continue
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
        """
        Set the access mode of all fields to optional (if the field doesn't exist, None is returned).
        """
        self.__strict_access = False

    def set_field_access_required(self):
        """
        Set the access mode of all fields to required (if the field doesn't exist, an exception is raised).
        """
        self.__strict_access = True

    def add_required_field(self, field_name: str):
        """
        Set the access mode of the given field to required (if the field doesn't exist, an exception is raised).
        :param field_name: The field whose access mode is set to required.
        """
        self.__field_access_settings[field_name] = True

    def add_required_fields(self, field_names: List[str]):
        """
        Set the access mode of the given fields to required (if the field doesn't exist, an exception is raised).
        :param field_names: List of fields whose access mode is set to required.
        """
        for field in field_names:
            self.add_required_field(field)

    def add_optional_field(self, field_name: str):
        """
        Set the access mode of the given field to optional (if the field doesn't exist, None is returned).
        :param field_name: The field whose access mode is set to required.
        """
        self.__field_access_settings[field_name] = False

    def add_optional_fields(self, field_names: List[str]):
        """
        Set the access mode of the given fields to optional (if the field doesn't exist, None is returned).
        :param field_names: List of fields whose access mode is set to required.
        """
        for field in field_names:
            self.add_optional_field(field)

    def parse_config(self, config: Union[str, dict]) -> Config:
        """
        Build the config. This method should be called last and uses the settings set via the other methods of this
        class (e.g., validate field type).
        :param config: Path to the config json file or a dictionary that contains the config values
        :return: The built config (that is validated and transformed according to the passed functions).
        """
        if isinstance(config, dict):
            config_dict = config
        else:
            with open(config, "r") as json_file:
                config_dict = json.load(json_file)

        if self.__json_schema is not None:
            jsonschema.validate(config_dict, self.__json_schema)
        self.__config = Config(config_dict,
                               strict_access=self.__strict_access,
                               required_fields=[field for field, status in self.__field_access_settings.items()
                                                if status],
                               optional_fields=[field for field, status in self.__field_access_settings.items()
                                                if not status])
        self.__validate_types()
        self.__validate_field_values()
        self.__transform_field_values()

        return self.__config




