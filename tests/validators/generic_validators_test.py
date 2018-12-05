from unittest import TestCase

from python_json_config.validators import is_valid_choice


class GenericValidatorsTest(TestCase):

    def test_is_valid_choice(self):
        list_validator = is_valid_choice([1, 2, "3"])
        self.assertTrue(list_validator(1))
        self.assertFalse(list_validator(3))
        self.assertTrue(list_validator("3"))
        self.assertFalse(list_validator(4))

        dict_validator = is_valid_choice({1: "2", "3": 4})
        self.assertTrue(dict_validator(1))
        self.assertFalse(dict_validator("2"))
        self.assertTrue(dict_validator("3"))
        self.assertFalse(dict_validator(4))
