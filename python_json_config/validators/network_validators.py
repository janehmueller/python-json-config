import socket


def is_ipv4_address(ip_address: str):
    """
    Tests if the given value is a valid IPv4 address
    :param ip_address: The ip address that is tested.
    :return: True if the passed address is a valid IPv4 address otherwise False.
    """
    try:
        socket.inet_aton(ip_address)
        return True
    except socket.error:
        return False


def is_unreserved_port(port: int):
    """
    Tests if the given port is an unreserved port.
    :param port: The port that is tested.
    :return: True if the port is not reserved otherwise False.
    """
    return port > 1023
