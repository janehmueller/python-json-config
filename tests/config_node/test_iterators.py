from unittest import TestCase

from python_json_config.config_node import ConfigNode


class ConfigNodeIteratorsTest(TestCase):

    def setUp(self):
        self.config_dict = {
            'key1': 1,
            'key2': {
                'key3': 3,
                'key4': { 'key5': 5 }
            }
        }

    def test_contains(self):
        config = ConfigNode(self.config_dict)
        self.assertTrue('key1' in config)
        self.assertFalse('key1.key2' in config)
        self.assertTrue('key2.key3' in config)
        self.assertTrue('key2.key4.key5' in config)
        self.assertFalse('key2.key4.key6' in config)
