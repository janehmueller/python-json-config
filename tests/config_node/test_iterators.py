from unittest import TestCase

from python_json_config.config_node import ConfigNode


class ConfigNodeIteratorsTest(TestCase):

    def setUp(self):
        self.config_dict = {
            'key1': 1,
            'key2': {
                'key3': 3,
                'key4': {'key5': 5},
                'key6': 6
            },
            'key7': 7
        }

    def test_contains(self):
        config = ConfigNode(self.config_dict)
        self.assertTrue('key1' in config)
        self.assertFalse('key1.key2' in config)
        self.assertTrue('key2.key3' in config)
        self.assertTrue('key2.key4.key5' in config)
        self.assertFalse('key2.key4.key6' in config)

    def test_keys(self):
        config = ConfigNode(self.config_dict)
        keys = list(config.keys())
        expected_keys = ['key1', 'key2.key3', 'key2.key4.key5', 'key2.key6', 'key7']
        self.assertEqual(keys, expected_keys)

    def test_values(self):
        config = ConfigNode(self.config_dict)
        values = list(config.values())
        self.assertEqual(values, [1, 3, 5, 6, 7])

    def test_items(self):
        config = ConfigNode(self.config_dict)
        items = list(config.items())
        expected_items = [('key1', 1), ('key2.key3', 3), ('key2.key4.key5', 5), ('key2.key6', 6), ('key7', 7)]
        self.assertEqual(items, expected_items)

    def test_iter(self):
        config = ConfigNode(self.config_dict)
        expected_keys = ['key1', 'key2.key3', 'key2.key4.key5', 'key2.key6', 'key7']
        self.assertEqual(list(config), expected_keys)

    def test_iteration(self):
        config = ConfigNode(self.config_dict)
        for iter_key, key, value, item in zip(config, config.keys(), config.values(), config.items()):
            item_key, item_value = item
            self.assertEqual(iter_key, key)
            self.assertEqual(item_key, key)
            self.assertEqual(item_value, value)
            self.assertEqual(config.get(key), value)

    def test_to_dict(self):
        config = ConfigNode(self.config_dict)
        self.assertEqual(config.to_dict(), self.config_dict)
        self.assertEqual(config.key2.to_dict(), self.config_dict["key2"])
        self.assertEqual(config.key2.key4.to_dict(), self.config_dict["key2"]["key4"])

