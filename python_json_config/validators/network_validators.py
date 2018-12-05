def is_timedelta(value: str) -> bool:
    """
    Checks if the given value is a valid timedelta specification.
    The timedelta needs to be specified as a colon separated string, e.g.: "0:0:23:00:00"
        The format is as follows "WW:DD:HH:MM:SS"
        W = number of months
        D = number of days
        H = number of hours
        M = number of minutes
        S = number of seconds
    :param value: the timedelta as string
    :return: True if the value is a valid timedelta specification otherwise False
    """
    if not isinstance(value, str):
        return False

    split_values = value.split(':')
    if len(split_values) != 5:
        return False

    try:
        [int(element) for element in split_values]
    except ValueError:
        return False

    return True
