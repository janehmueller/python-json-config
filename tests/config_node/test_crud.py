import os
import warnings
from unittest import TestCase

from python_json_config.config_node import ConfigNode


class ConfigNodeCrudTest(TestCase):

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
        with self.assertRaises(AttributeError):
            node.nokey

        self.assertEqual(node.get('key1'), 1)
        with self.assertRaises(AttributeError): node.get('nokey')

        self.assertEqual(node.get('key2.key3'), 3)

    def test_add(self):
        node = ConfigNode({'key1': 1})
        self.assertEqual(node.key1, 1)

        with self.assertRaises(AttributeError):
            node.key2
        node.add('key2', 2)
        self.assertEqual(node.key2, 2)

        with self.assertRaises(AttributeError):
            node.key3.key4
        node.add('key3.key4', "test")
        self.assertEqual(node.key3.key4, "test")

    def test_add_overwrite(self):
        node = ConfigNode({'key1': 1})
        self.assertEqual(node.key1, 1)

        with warnings.catch_warnings(record=True) as warning_log:
            self.assertEqual(len(warning_log), 0)

            node.add('key1', 2, overwrite=False)
            self.assertEqual(len(warning_log), 1)
            self.assertEqual(node.key1, 2)

            node.add('key1', 3)
            self.assertEqual(len(warning_log), 1)
            self.assertEqual(node.key1, 3)

    def test_update(self):
        node = ConfigNode(self.config_dict)

        self.assertEqual(node.key1, 1)
        node.update('key1', 2)
        self.assertEqual(node.key1, 2)

        node.update('key1', {'newkey': 1})
        self.assertIsInstance(node.key1, ConfigNode)
        self.assertEqual(node.key1.newkey, 1)

        self.assertIsInstance(node.key2.key4, ConfigNode)
        node.update('key2.key4', 1337)
        self.assertEqual(node.key2.key4, 1337)

    def test_update_upsert(self):
        node = ConfigNode({'key1': 1})

        with self.assertRaises(AttributeError):
            node.key2

        with self.assertRaises(RuntimeError):
            node.update('key2', 'asd', upsert=False)

        node.update('key2', 'asd', upsert=True)
        self.assertEqual(node.key2, 'asd')

    def test_strict_access(self):
        config = ConfigNode(self.config_dict,
                            strict_access=True,
                            optional_fields=['nokey', ['key2', 'nokey'], 'key2.nokey2'])
        self.assertIsNone(config.nokey)
        self.assertIsNone(config.key2.nokey)
        self.assertIsNone(config.key2.nokey2)
        with self.assertRaises(AttributeError):
            config.key2.nokey3

        config = ConfigNode(self.config_dict,
                            strict_access=False,
                            required_fields=['nokey', ['key2', 'nokey'], 'key2.nokey2'])
        self.assertIsNone(config.key2.nokey3)
        with self.assertRaises(AttributeError):
            self.assertIsNone(config.nokey)
        with self.assertRaises(AttributeError):
            self.assertIsNone(config.key2.nokey)
        with self.assertRaises(AttributeError):
            self.assertIsNone(config.key2.nokey2)

    def test_merge_env_variable(self):
        prefix = "PYTHONJSONCONFIG"
        variables = {f"{prefix}_TESTVALUE1": "bla", f"{prefix}_TESTVALUE2": "1"}
        for key, value in variables.items():
            os.environ[key] = value

        config = ConfigNode({"testvalue1": "blub", "testvalue3": 5})
        config.merge_with_env_variables(prefix)

        self.assertEqual(config.testvalue1, "bla")
        self.assertEqual(config.testvalue2, "1")
        self.assertEqual(config.testvalue3, 5)

        for key, value in variables.items():
            del os.environ[key]
