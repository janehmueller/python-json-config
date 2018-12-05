from unittest import TestCase

from python_json_config.validators import is_ipv4_address, is_unreserved_port


class NetworkValidatorsTest(TestCase):

    def test_is_ipv4_address(self):
        valid_ips = ["127.0.0.1", "8.8.8.8", "127.1", "8.526344"]
        invalid_ips = ["327.0.0.1", "8.8.8.8.8", "127.-1", "256.526344"]

        for address in valid_ips:
            self.assertTrue(is_ipv4_address(address))

        for address in invalid_ips:
            self.assertFalse(is_ipv4_address(address))

    def test_is_unreserved_port(self):
        self.assertFalse(is_unreserved_port(1))
        self.assertFalse(is_unreserved_port(-1))
        self.assertFalse(is_unreserved_port(22))
        self.assertFalse(is_unreserved_port(1023))
        self.assertTrue(is_unreserved_port(1024))
        self.assertTrue(is_unreserved_port(14302))
