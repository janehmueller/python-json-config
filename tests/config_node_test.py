from unittest import TestCase

from src.config_node import ConfigNode


class ConfigNodeTest(TestCase):

    def setUp(self):
        self.config_dict = {
            "key1": 1,
            "key2": {
                "key3": 3,
                "key4": { "key5": 5 }
            }
        }

    def test_creation(self):
        node = ConfigNode(self.config_dict)
        self.assertEqual(node.key1, 1)
        self.assertEqual(node.__dict__["_ConfigNode__path"], [])
        self.assertIsInstance(node.key2, ConfigNode)

        nested_node = node.key2
        self.assertEqual(nested_node.key3, 3)
        self.assertEqual(nested_node.__dict__["_ConfigNode__path"], ["key2"])
        self.assertIsInstance(nested_node.key4, ConfigNode)

        nested_node = nested_node.key4
        self.assertEqual(nested_node.key5, 5)
        self.assertEqual(nested_node.__dict__["_ConfigNode__path"], ["key2", "key4"])

    def test_get(self):
        node = ConfigNode(self.config_dict)
        self.assertEqual(node.key1, 1)
        with self.assertRaises(KeyError): node.nokey

        self.assertEqual(node.get("key1"), 1)
        with self.assertRaises(KeyError): node.get("nokey")

    def test_update(self):
        node = ConfigNode(self.config_dict)
        self.assertEqual(node.key1, 1)
        node.update("key1", 2)
        self.assertEqual(node.key1, 2)

        node.update("key1", {"newkey": 1})
        self.assertIsInstance(node.key1, ConfigNode)
        self.assertEqual(node.key1.newkey, 1)

        with self.assertRaises(KeyError): node.key3
        node.update("key3", "asd")
        self.assertEqual(node.key3, "asd")

        self.assertIsInstance(node.key2.key4, ConfigNode)
        node.update("key2.key4", 1337)
        self.assertEqual(node.key2.key4, 1337)

    def test_string(self):
        node = ConfigNode({1: 2, 3: 4})
        node_str = "ConfigNode(path=[], values={1: 2, 3: 4})"
        self.assertEqual(str(node), node_str)
