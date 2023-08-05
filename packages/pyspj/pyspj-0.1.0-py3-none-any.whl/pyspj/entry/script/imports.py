from hbutils.reflection import import_object

_DEFAULT_FUNC_NAME = '__spj__'


def _load_func_from_string(string: str):
    splits = string.split(":", maxsplit=1)
    if len(splits) == 1:
        package_name, func_name = splits[0], _DEFAULT_FUNC_NAME
    else:
        package_name, func_name = splits

    return import_object(func_name, package_name)


def _load_func(data):
    """
    load function from any kind of data
    :param data: raw data
    :return: loaded function
    """

    if isinstance(data, str):
        _func = _load_func_from_string(data)
    else:
        _func = data

    if not callable(_func):
        raise TypeError(
            'Callable type expected but {actual} found.'.format(actual=repr(type(_func).__name__)))

    return _func
