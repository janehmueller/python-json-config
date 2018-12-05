from typing import List, Union

from .utils import normalize_path


class ConfigNode(object):
    def __init__(self, config_dict: dict, path: List[str] = None):
        self.__path = path or []
        node_dict = {}
        for key, value in config_dict.items():
            if isinstance(value, dict):
                node_dict[key] = ConfigNode(value, path=self.__path + [key])
            else:
                node_dict[key] = value

        self.__node_dict = node_dict

    def __getattr__(self, item: str):
        return self.get(item)

    def get(self, path: Union[str, List[str]]):
        """
        Retrieve a value in the config. If the referenced field does not exist an KeyError is thrown.
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
        return f'ConfigNode(path={self.__path}, values={self.__node_dict})'

    __repr__ = __str__

    """
    These two methods are needed to enable pickling since this class overwrites __getattr__.
    """
    def __getstate__(self):
        return vars(self)

    def __setstate__(self, state):
        vars(self).update(state)


class Config(ConfigNode):
    def __init__(self, config_dict: dict):
        super(Config, self).__init__(config_dict, [])
