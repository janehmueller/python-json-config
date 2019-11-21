import re
from typing import Union, List


def normalize_path(path: Union[str, List[str]]) -> List[str]:
    if isinstance(path, str):
        path = path.split(".")
    return path


def parse_env_variable_name(variable: str) -> List[str]:
    """
    Parse the name of an environment variable into a config path. Underscores in the names of variables are escaped with
    an extra underscore. (E.g., the field test_value will be set by the variable TEST__VALUE).
    :param variable: the name of the environment variable
    :return: the path extracted from the name of the environment variable
    """
    # Split only on single underscores
    split_variable = re.sub(r"([^_])[_]([^_])", r"\1 \2", variable.lower()).split(" ")
    path = [element for element in split_variable if element]

    # If the path contains single elements only consisting of underscores, join the previous and next element together.
    # (e.g., ["test", "__", "value"] becomes ["test__value"])
    underscore_indices = [i for i, item in enumerate(path) if re.search("^_+$", item)]
    for index in underscore_indices:
        path[index - 1:index + 2] = ["".join(path[index - 1:index + 2])]

    # Remove the extra underscore from names containing underscores (that was used to escape the underscore).
    # (e.g., ["test__value"] becomes ["test_value"])
    for index, element in enumerate(path):
        if "_" in element:
            underscore_match = re.search("[_]+", element)
            underscores = underscore_match.group(0)
            if len(underscores) > 1:
                path[index] = element.replace(underscores, underscores[:-1])

    return path
