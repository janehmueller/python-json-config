import socket


def is_timedelta(value: str) -> bool:
    """
    Tests if the given value is a valid timedelta specification.
    The timedelta needs to be specified as a colon separated string, e.g.: "0:0:23:00:00"
        The format is as follows "WW:DD:HH:MM:SS"
        W = number of months
        D = number of days
        H = number of hours
        M = number of minutes
        S = number of seconds
    :param value: The timedelta as string.
    :return: True if the value is a valid timedelta specification otherwise False.
    """
    split_values = value.split(':')
    if len(split_values) != 5:
        return False

    try:
        [int(element) for element in split_values]
    except ValueError:
        return False

    return True


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
