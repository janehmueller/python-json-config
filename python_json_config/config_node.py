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

    def __getattr__(self, item):
        return self.get(item)

    def get(self, path: Union[str, List[str]]):
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
            raise KeyError(f'No value exists for key "{print_path}{key}"') from exception

    def update(self, path: Union[str, List[str]], value):
        path = normalize_path(path)
        key = path[0]
        if len(path) == 1:
            if isinstance(value, dict):
                self.__node_dict[key] = ConfigNode(value, path=self.__path + [key])
            else:
                self.__node_dict[key] = value
        else:
            self.get(key).update(path[1:], value)

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
