import pickle
from unittest import TestCase

from python_json_config.config_node import ConfigNode


class ConfigNodeSerializationTest(TestCase):

    def setUp(self):
        self.config_dict = {
            'key1': 1,
            'key2': {
                'key3': 3,
                'key4': { 'key5': 5 }
            }
        }

    def test_pickle(self):
        config = ConfigNode(self.config_dict)
        pickle_conf = pickle.loads(pickle.dumps(config))
        self.assertEqual(pickle_conf.key1, 1)
        self.assertEqual(pickle_conf.key2.key3, 3)
        self.assertEqual(pickle_conf.key2.key4.key5, 5)
