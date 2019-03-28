from python_json_config.config_node import ConfigNode


def test_string():
    node = ConfigNode({1: 2, 3: 4})
    node_str = 'ConfigNode(path=[], values={1: 2, 3: 4}, strict_access=True, required_fields=[], optional_fields' \
               '=[])'
    assert str(node) == node_str
