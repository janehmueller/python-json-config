from unittest import TestCase

from python_json_config.validators import is_timedelta


class NetworkValidatorsTest(TestCase):

    def test_is_timedelta(self):
        valid_timedeltas = ["1:3:24:30:23", "0:0:0:0:1", "01:02:02:03:04"]
        invalid_timedeltas = ["1:3:24:30:23:45", "0:0:1", "01:a:02:03:04"]

        for timedelta in valid_timedeltas:
            self.assertTrue(is_timedelta(timedelta))

        for timedelta in invalid_timedeltas:
            self.assertFalse(is_timedelta(timedelta))
