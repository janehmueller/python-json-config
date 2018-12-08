from unittest import TestCase

from python_json_config.validators import is_timedelta, is_valid_choice


class GenericValidatorsTest(TestCase):

    def test_is_timedelta(self):
        valid_timedeltas = ['1:3:24:30:23', '0:0:1', '0:0:0:0:1', '01:02:02:03:04']
        invalid_timedeltas = ['1:3:24:30:23:45', '01:a:02:03:04']

        for timedelta in valid_timedeltas:
            self.assertTrue(is_timedelta(timedelta))

        self.assertEqual(is_timedelta(invalid_timedeltas[0]), (False, 'Timedelta contains more than 5 elements.'))
        self.assertEqual(is_timedelta(invalid_timedeltas[1]), (False, 'Timedelta contains non-integer elements.'))


    def test_is_valid_choice(self):
        list_options = [1, 2, '3']
        list_validator = is_valid_choice(list_options)
        self.assertTrue(list_validator(1))
        self.assertEqual(list_validator(3), (False, f'Value is not contained in the options {list_options}'))
        self.assertTrue(list_validator('3'))
        self.assertEqual(list_validator(4), (False, f'Value is not contained in the options {list_options}'))

        dict_options = {1: '2', '3': 4}
        dict_validator = is_valid_choice(dict_options)
        self.assertTrue(dict_validator(1))
        self.assertEqual(dict_validator('2'), (False, f'Value is not contained in the options {dict_options}'))
        self.assertTrue(dict_validator('3'))
        self.assertEqual(dict_validator(4), (False, f'Value is not contained in the options {dict_options}'))
