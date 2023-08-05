from typing import Mapping

from ...utils import list_to_envs

_FORBIDDEN_NAMES = {'stdin', 'stdout'}


def _check_values(values: Mapping[str, str]) -> Mapping[str, str]:
    """
    check value dict
    :param values: value dict
    :return: value dict
    """
    for name in _FORBIDDEN_NAMES:
        if name in values.keys():
            raise KeyError('Value should not be named as {name}.'.format(name=repr(name)))

    return values


def _load_from_values(values) -> Mapping[str, str]:
    """
    load values from list of strings
    :param values: list of strings
    :return: string dict
    """
    return _check_values(list_to_envs(values))
