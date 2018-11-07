from functools import reduce
from typing import Union, List

from src.config_node import ConfigNode


class Config(ConfigNode):
    def __init__(self, config_dict: dict):
        super(Config, self).__init__(config_dict, [])

    def __normalize_path(self, path: Union[str, List[str]]) -> List[str]:
        if isinstance(path, str):
            path = path.split(".")
        return path

    def traverse_path(self, path: Union[str, List[str]]):
        return reduce(lambda node, path: node.get(path), self.__normalize_path(path), self)

    def update_path(self, path: Union[str, List[str]], value):
        path = self.__normalize_path(path)
        node = reduce(lambda node, path: node.get(path), path[:-1], self)
        node.update(path[-1], value)
