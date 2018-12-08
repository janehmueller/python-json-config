from unittest import TestCase

from python_json_config.validators import is_ipv4_address, is_unreserved_port


class NetworkValidatorsTest(TestCase):

    def test_is_ipv4_address(self):
        valid_ips = ['127.0.0.1', '8.8.8.8', '127.1', '8.526344']
        invalid_ips = ['327.0.0.1', '8.8.8.8.8', '127.-1', '256.526344']

        for address in valid_ips:
            self.assertTrue(is_ipv4_address(address))

        for address in invalid_ips:
            self.assertEqual(is_ipv4_address(address), (False, 'IP address is not a valid IPv4 address.'))

    def test_is_unreserved_port(self):
        self.assertEqual(is_unreserved_port(1), (False, 'Port is reserved.'))
        self.assertEqual(is_unreserved_port(-1), (False, 'Port is reserved.'))
        self.assertEqual(is_unreserved_port(22), (False, 'Port is reserved.'))
        self.assertEqual(is_unreserved_port(1023), (False, 'Port is reserved.'))
        self.assertTrue(is_unreserved_port(1024))
        self.assertTrue(is_unreserved_port(14302))
