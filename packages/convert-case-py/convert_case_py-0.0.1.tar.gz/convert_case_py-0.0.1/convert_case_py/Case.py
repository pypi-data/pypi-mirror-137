import re


def camelcase_to_lowercase(data):
    """


    :param data:
    :return:
    """

    """Convert all keys to lowercase"""
    result = {}
    for key, value in data.items():
        try:
            result[key.lower()] = camelcase_to_lowercase(value) if type(value) is dict else value
        except AttributeError:
            result[key] = value
    return result


def snakecase_to_lowercase(data):
    """


    :param data:
    :return:
    """

    """Convert all keys to lowercase"""
    result = {}
    for key, value in data.items():
        try:
            result[key.replace('_', '').lower()] = snakecase_to_lowercase(value) if type(value) is dict else value
        except AttributeError:
            result[key] = value
    return result


def snakecase_to_camelcase(data, pascal_mode=False):
    """


    :param data:
    :param pascal_mode:
    :return:
    """

    result = {}
    for key, value in data.items():
        try:
            if pascal_mode:
                new_key = ''.join(x.capitalize() or '_' for x in key.split('_'))
                result[new_key] = snakecase_to_camelcase(value, True) if type(value) is dict else value
            else:
                new_key = ''.join(x.capitalize() or '_' for x in key.split('_'))

                new_key_list = list(new_key)
                new_key_list[0] = new_key_list[0].lower()

                new_key = ''.join(new_key_list)

                result[new_key] = snakecase_to_camelcase(value) if type(value) is dict else value
        except AttributeError:
            result[key] = value
    return result


def camelcase_to_snakecase(data, pascal_mode=False):
    """


    :param data:
    :param pascal_mode:
    :return:
    """

    result = {}
    for key, value in data.items():
        try:
            key = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
            key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
            if pascal_mode:
                result[key] = camelcase_to_snakecase(value, True) if type(value) is dict else value
            else:
                result[key] = camelcase_to_snakecase(value) if type(value) is dict else value
        except AttributeError:
            result[key] = value
    return result


def snakecase_to_pascalcase(data):
    """


    :param data:
    :return:
    """

    return snakecase_to_camelcase(data, True)


def pascalcase_to_snakecase(data):
    """


    :param data:
    :return:
    """

    return camelcase_to_snakecase(data, True)
