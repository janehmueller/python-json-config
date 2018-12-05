import pickle
from unittest import TestCase

from python_json_config.config_node import ConfigNode


class ConfigNodeTest(TestCase):

    def setUp(self):
        self.config_dict = {
            'key1': 1,
            'key2': {
                'key3': 3,
                'key4': { 'key5': 5 }
            }
        }

    def test_creation(self):
        node = ConfigNode(self.config_dict)
        self.assertEqual(node.key1, 1)
        self.assertEqual(node.__dict__['_ConfigNode__path'], [])
        self.assertIsInstance(node.key2, ConfigNode)

        nested_node = node.key2
        self.assertEqual(nested_node.key3, 3)
        self.assertEqual(nested_node.__dict__['_ConfigNode__path'], ['key2'])
        self.assertIsInstance(nested_node.key4, ConfigNode)

        nested_node = nested_node.key4
        self.assertEqual(nested_node.key5, 5)
        self.assertEqual(nested_node.__dict__['_ConfigNode__path'], ['key2', 'key4'])

    def test_get(self):
        node = ConfigNode(self.config_dict)
        self.assertEqual(node.key1, 1)
        with self.assertRaises(AttributeError): node.nokey

        self.assertEqual(node.get('key1'), 1)
        with self.assertRaises(AttributeError): node.get('nokey')

        self.assertEqual(node.get('key2.key3'), 3)

    def test_update(self):
        node = ConfigNode(self.config_dict)
        self.assertEqual(node.key1, 1)
        node.update('key1', 2)
        self.assertEqual(node.key1, 2)

        node.update('key1', {'newkey': 1})
        self.assertIsInstance(node.key1, ConfigNode)
        self.assertEqual(node.key1.newkey, 1)

        with self.assertRaises(AttributeError): node.key3
        node.update('key3', 'asd')
        self.assertEqual(node.key3, 'asd')

        self.assertIsInstance(node.key2.key4, ConfigNode)
        node.update('key2.key4', 1337)
        self.assertEqual(node.key2.key4, 1337)

    def test_string(self):
        node = ConfigNode({1: 2, 3: 4})
        node_str = 'ConfigNode(path=[], values={1: 2, 3: 4})'
        self.assertEqual(str(node), node_str)

    def test_pickle(self):
        config = ConfigNode(self.config_dict)
        pickle_conf = pickle.loads(pickle.dumps(config))
        self.assertEqual(pickle_conf.key1, 1)
        self.assertEqual(pickle_conf.key2.key3, 3)
        self.assertEqual(pickle_conf.key2.key4.key5, 5)

    def test_contains(self):
        config = ConfigNode(self.config_dict)
        self.assertTrue('key1' in config)
        self.assertFalse('key1.key2' in config)
        self.assertTrue('key2.key3' in config)
        self.assertTrue('key2.key4.key5' in config)
        self.assertFalse('key2.key4.key6' in config)
