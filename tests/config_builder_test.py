from unittest import TestCase

from python_json_config import ConfigBuilder


class ConfigBuilderTest(TestCase):

    def setUp(self):
        self.path = 'tests/resources/test_config.json'

    def test_parse(self):
        config = ConfigBuilder()\
            .validate_field_type('server.port', int)\
            .validate_field_value('server.debug_mode', lambda x: not x)\
            .transform_field_value('server.port', lambda x: str(x))\
            .parse_config(self.path)
        self.assertIsNotNone(config)
        self.assertFalse(config.server.debug_mode)
        self.assertEqual(config.server.port, '5000')

    def test_type_validation_builder(self):
        builder = ConfigBuilder()
        builder.validate_field_type('key1', int)
        builder.validate_field_type('key1.key2', list)
        type_validation_dict = builder._ConfigBuilder__validation_types
        self.assertEqual(type_validation_dict['key1'], int)
        self.assertEqual(type_validation_dict['key1.key2'], list)

    def test_value_validation_builder(self):
        builder = ConfigBuilder()
        builder.validate_field_value('key1', lambda x: x < 4)
        builder.validate_field_value('key1.key2', lambda x: len(x) == 3)
        value_validation_dict = builder._ConfigBuilder__validation_functions
        self.assertTrue(value_validation_dict['key1'](1))
        self.assertFalse(value_validation_dict['key1'](4))
        self.assertTrue(value_validation_dict['key1.key2']([1, 2, 3]))
        self.assertFalse(value_validation_dict['key1.key2'](['a', 'b']))

    def test_value_transformation_builder(self):
        builder = ConfigBuilder()
        builder.transform_field_value('key1', lambda x: x * 4)
        builder.transform_field_value('key1.key2', lambda x: [x[len(x) - 1 - i] for i in range(len(x))])
        value_transformation_dict = builder._ConfigBuilder__transformation_functions
        self.assertEqual(value_transformation_dict['key1'](1), 4)
        self.assertEqual(value_transformation_dict['key1'](4), 16)
        self.assertEqual(value_transformation_dict['key1.key2']([1, 2, 3]), [3, 2, 1])
        self.assertEqual(value_transformation_dict['key1.key2'](['a', 'b', False]), [False, 'b', 'a'])

    def test_type_validation(self):
        builder = ConfigBuilder()
        builder.validate_field_type('server.debug_mode', bool)
        builder.validate_field_type('server.port', int)
        builder.parse_config(self.path)
        builder.validate_field_type('server.host', int)
        with self.assertRaises(AssertionError): builder.parse_config(self.path)

    def test_value_validation(self):
        builder = ConfigBuilder()
        builder.validate_field_value('server.debug_mode', lambda x: not x)
        builder.validate_field_value('server.port', lambda x: x < 10000)
        builder.parse_config(self.path)
        builder.validate_field_value('cache.ttl', lambda x: x > 200)
        with self.assertRaises(AssertionError): builder.parse_config(self.path)

    def test_value_transformation(self):
        builder = ConfigBuilder()
        config = builder.parse_config(self.path)
        self.assertFalse(config.server.debug_mode)
        self.assertEqual(config.server.port, 5000)

        builder.transform_field_value('server.debug_mode', lambda x: not x)
        builder.transform_field_value('server.port', lambda x: x + 4)
        config = builder.parse_config(self.path)
        self.assertTrue(config.server.debug_mode)
        self.assertEqual(config.server.port, 5004)


