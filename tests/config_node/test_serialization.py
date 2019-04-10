import pickle

from python_json_config.config_node import ConfigNode


def test_pickle(config_dict):
    config = ConfigNode(config_dict)
    pickle_conf = pickle.loads(pickle.dumps(config))
    assert pickle_conf.key1 == 1
    assert pickle_conf.key2.key3 == 3
    assert pickle_conf.key2.key4.key5 == 5


def test_to_dict(config_dict):
    config = ConfigNode(config_dict)
    assert config.to_dict() == config_dict
    assert config.key2.to_dict() == config_dict["key2"]
    assert config.key2.key4.to_dict() == config_dict["key2"]["key4"]


def test_to_json(config_dict):
    config = ConfigNode(config_dict)
    json = config.to_json()
    assert json == """{"key1": 1, "key2": {"key3": 3, "key4": {"key5": 5}, "key6": 6}, "key7": 7}"""
