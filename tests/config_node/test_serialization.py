import pickle

from python_json_config.config_node import ConfigNode


def test_pickle(config_dict):
    config = ConfigNode(config_dict)
    pickle_conf = pickle.loads(pickle.dumps(config))
    assert pickle_conf.key1 == 1
    assert pickle_conf.key2.key3 == 3
    assert pickle_conf.key2.key4.key5 == 5
