from unittest import TestCase

from python_json_config.config_node import ConfigNode


class ConfigNodeUtilsTest(TestCase):
    def test_string(self):
        node = ConfigNode({1: 2, 3: 4})
        node_str = 'ConfigNode(path=[], values={1: 2, 3: 4}, strict_access=True, required_fields=[], optional_fields' \
                   '=[])'
        self.assertEqual(str(node), node_str)
