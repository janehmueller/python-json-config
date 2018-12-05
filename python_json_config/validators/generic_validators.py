def is_valid_choice(options):
    """
    Returns a function that tests if the config value is an element of the passed options.
    :param options: The options that are considered as valid choices.
    :return: A functions that takes a value and tests if it is within the specified choices. This function returns True
             if the value in the config is in the passed options.
    """
    def validator(value):
        return value in options

    return validator
