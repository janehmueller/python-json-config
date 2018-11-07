from typing import List, Union


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

    def get(self, key):
        try:
            return self.__node_dict[key]
        except KeyError:
            raise KeyError(f'No value exists for key "{".".join(self.__path)}.{key}""')


    def update(self, path: Union[str, List[str]], value):
        if isinstance(path, str):
            path = path.split(".")
        key = path[0]
        if len(path) == 1:
            if isinstance(value, dict):
                self.__node_dict[key] = ConfigNode(value, path=self.__path + [key])
            else:
                self.__node_dict[key] = value
        else:
            self.get(key).update(path[1:], value)

    def __str__(self):
        return f"ConfigNode(path={self.__path}, values={self.__node_dict})"

    __repr__ = __str__
