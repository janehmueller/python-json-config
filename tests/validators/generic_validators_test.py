from unittest import TestCase

from python_json_config.validators import is_timedelta, is_valid_choice


class GenericValidatorsTest(TestCase):

    def test_is_timedelta(self):
        valid_timedeltas = ["1:3:24:30:23", "0:0:1", "0:0:0:0:1", "01:02:02:03:04"]
        invalid_timedeltas = ["1:3:24:30:23:45", "01:a:02:03:04"]

        for timedelta in valid_timedeltas:
            self.assertTrue(is_timedelta(timedelta))

        for timedelta in invalid_timedeltas:
            self.assertFalse(is_timedelta(timedelta))

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
