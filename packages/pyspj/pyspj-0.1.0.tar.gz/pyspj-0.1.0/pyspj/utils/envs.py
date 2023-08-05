from typing import List, Mapping


def string_to_env(string: str):
    """
    Overview:
        Turn string ``KEY=VALUE`` to key-value tuple.

    Arguments:
        - string (:obj:`str`): Original key-value string.

    Returns:
        - (key, value): key and value

    Examples::
        >>> from pyspj.utils import string_to_env
        >>> string_to_env('THIS=1')
        ('THIS', '1')
        >>> string_to_env('THIS=1=2')
        ('THIS', '1=2')
    """
    _name, _value = string.split('=', maxsplit=1)
    return _name, _value


def list_to_envs(strings: List[str]) -> Mapping[str, str]:
    """
    Overview:
        Turn a list of strings to key-value dict.

    Arguments:
        - strings (:obj:`List[str]`): List of key-value strings.

    Returns:
        - envs (:obj:`Mapping[str, str]`): Separated key-value dict.

    Examples::
        >>> from pyspj.utils import list_to_envs
        >>> list_to_envs([
        ...     '1=2',
        ...     'THIS=',
        ...     'OK=kjsdlf-2398',
        ...     'THISX=1=2',
        ... ])
        {'1': '2', 'THIS': '', 'OK': 'kjsdlf-2398', 'THISX': '1=2'}
    """
    return {key: value for key, value in map(string_to_env, strings)}


def env_to_string(name, value) -> str:
    """
    Overview:
        Turn key and value to ``KEY=VALUE`` string.

    Arguments:
        - name (:obj:`str`): Name of key.
        - value (:obj:`str`): Value.

    Returns:
        - string (:obj:`str`): ``KEY=VALUE`` string.

    Examples::
        >>> from pyspj.utils import env_to_string
        >>> env_to_string('THIS', '')
        'THIS='
        >>> env_to_string('THIS', '1=2')
        'THIS=1=2'
    """
    return f'{name}={value}'


def envs_to_list(envs: Mapping[str, str]) -> List[str]:
    """
    Overview:
        Turn key-value dict to list of ``KEY=VALUE`` strings.

    Arguments:
        - envs (:obj:`Mapping[str, str]`): Key-value dict.

    Returns:
        - lenvs (:obj:`List[str]`): List of ``KEY=VALUE`` strings.

    Examples::
        >>> from pyspj.utils import envs_to_list
        >>> envs_to_list({
        ...     '1': '2',
        ...     'THIS': '',
        ...     'OK': 'kjsdlf-2398',
        ...     'THISX': '1=2',
        ... })
        ['1=2', 'THIS=', 'OK=kjsdlf-2398', 'THISX=1=2']
    """
    return [env_to_string(_name, _value) for _name, _value in envs.items()]
