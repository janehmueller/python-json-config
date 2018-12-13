from typing import List, Union, Tuple

from .utils import normalize_path


class ConfigNode(object):
    def __init__(self,
                 config_dict: dict,
                 path: List[str] = None,
                 strict_access: bool = True,
                 required_fields: List[Union[str, List[str]]] = None,
                 optional_fields: List[Union[str, List[str]]] = None):
        """
        Create a node in the Config Tree. This node will create its children if there are nested objects in the config.
        :param config_dict: Source dictionary containing the part of the config that will be in this node and its
                            children. Each dictionary value in this dictionary will become another ConfigNode that is
                            a child of this node.
        :param path: The access path to this node, i.e. the config keys that are used to access thos node.
        :param strict_access: If True, an error will be thrown if a non-existing field is accessed. If False,
                                    None will be returned instead.
        :param required_fields: A list of field names, for which an error will be thrown if they are accessed but don't
                                exist. These names either contain dots for the subfields or are already normalized
                                paths.
        :param optional_fields: A list of field names, for which None will be returned if they are accessed but don't
                                exist. These names either contain dots for the subfields or are already normalized
                                paths.
        """
        self.__path = path or []
        self.strict_access = strict_access

        self.required_fields, required_subfields = self.__parse_field_settings(required_fields or [])
        self.optional_fields, optional_subfields = self.__parse_field_settings(optional_fields or [])

        # parse the config dictionary and create children if necessary
        node_dict = {}
        for key, value in config_dict.items():
            if isinstance(value, dict):
                node_dict[key] = ConfigNode(value,
                                            path=self.__path + [key],
                                            strict_access=strict_access,
                                            required_fields=required_subfields,
                                            optional_fields=optional_subfields)
            else:
                node_dict[key] = value

        self.__node_dict = node_dict

    def __getattr__(self, item: str):
        """
        Enables access of config elements via dots (i.e. config.field1 instead of config["field1"]). This method wraps
        the get method.
        If strict access is defined or the field is a required field, an AttributeError is thrown if the referenced
        field does not exist. Otherwise, i.e. non-strict access is defined or the field is an optional field, None is
        returned in the field does not exist.
        :raises AttributeError: Raised when a non-existing field is accessed when either strict access is defined or the
                                field is a required field.
        :param item: the field that is accessed.
        :return: The value of the referenced field.
        """
        return self.get(item)

    def get(self, path: Union[str, List[str]]):
        """
        Retrieve a value in the config.
        If strict access is defined or the field is a required field, an AttributeError is thrown if the referenced
        field does not exist. Otherwise, i.e. non-strict access is defined or the field is an optional field, None is
        returned in the field does not exist.
        :raises AttributeError: Raised when a non-existing field is accessed when either strict access is defined or the
                                field is a required field.
        :param path: The key of the field. Can be either a string with '.' as delimiter of the nesting levels or a list
                     of keys with each element being one nesting level.
                     E.g., the string 'key1.key2' and list ['key1', 'key2'] reference the same config element.
        :return: The value of the referenced field.
        """
        path = normalize_path(path)
        key = path[0]
        try:
            value = self.__node_dict[key]
            if len(path) == 1:
                return value
            else:
                return value.get(path[1:])
        except KeyError as exception:
            if key in self.optional_fields or (not self.strict_access and key not in self.required_fields):
                return None
            else:
                print_path = '.'.join(self.__path) + ('.' if len(self.__path) > 0 else '')
                raise AttributeError(f'No value exists for key "{print_path}{key}"') from exception

    def update(self, path: Union[str, List[str]], value) -> None:
        """
        Update field in the config.
        :param path: The name of the field. Can be either a string with '.' as delimiter of the nesting levels or a list
                     of keys with each element being one nesting level.
                     E.g., the string 'key1.key2' and list ['key1', 'key2'] reference the same config element.
        :param value: The value that should replace the old value. If this value is a dictionary it is transformed into
                      a ConfigNode.
        """
        path = normalize_path(path)
        key = path[0]
        if len(path) == 1:
            if isinstance(value, dict):
                self.__node_dict[key] = ConfigNode(value, path=self.__path + [key])
            else:
                self.__node_dict[key] = value
        else:
            self.get(key).update(path[1:], value)

    def __contains__(self, item: Union[str, List[str]]) -> bool:
        """
        Test if a field exists in the config and is not None (result in the case of a non-existing optional field).
        If the field does not exist, an AttributeError is thrown, and therefore False is returned.
        :param item: The field whose existence is tested. Can be either a string with '.' as delimiter of the nesting
                     levels or a list of keys with each element being one nesting level.
                     E.g., the string 'key1.key2' and list ['key1', 'key2'] reference the same config element.
        :return: True if the field exists in the Config and False otherwise.
        """
        try:
            result = self.get(item)
            return result is not None
        except AttributeError:
            return False

    def __str__(self):
        return f'ConfigNode(path={self.__path}, values={self.__node_dict}, strict_access={self.strict_access}, ' \
               f'required_fields={self.required_fields}, optional_fields={self.optional_fields})'

    __repr__ = __str__

    def __getstate__(self):
        """
        This method is needed to enable pickling since this class overwrites __getattr__.
        """
        return vars(self)

    def __setstate__(self, state):
        """
        This method is needed to enable pickling since this class overwrites __getattr__.
        """
        vars(self).update(state)

    def __parse_field_settings(self, field_names: List[Union[str, List[str]]]) -> Tuple[List[str], List[List[str]]]:
        """
        Parses settings (required or optional) for fields and subfields of this node.
        :param field_names: A list of either field names containing dots or already normalized paths.
        :return: A tuple of first a list of the field names that are in this node and secondly a list of normalized
                 paths of subfields (i.e., fields in children of this node).
        """
        settings = []
        subfield_settings = []
        normalized_fields = [normalize_path(field) for field in field_names]
        for path in normalized_fields:
            if len(path) == 1:
                settings.append(path[0])
            else:
                subfield_settings.append(path[1:])
        return settings, subfield_settings


class Config(ConfigNode):
    def __init__(self, config_dict: dict,
                 strict_access: bool = True,
                 required_fields: List[Union[str, List[str]]] = None,
                 optional_fields: List[Union[str, List[str]]] = None):
        super(Config, self).__init__(config_dict,
                                     path=[],
                                     strict_access=strict_access,
                                     required_fields=required_fields,
                                     optional_fields=optional_fields)
