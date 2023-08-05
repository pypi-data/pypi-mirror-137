from enum import unique, IntEnum
from typing import Tuple, Optional

import enum_tools
from hbutils.model import int_enum_loads

from .base import SPJResult
from .continuity import ContinuitySPJResult
from .simple import SimpleSPJResult


def _load_from_values(correctness, score, message, detail) -> SPJResult:
    if score is None:
        return SimpleSPJResult(correctness, message, detail)
    else:
        return ContinuitySPJResult(correctness, score, message, detail)


def _load_result_from_dict(data: dict) -> SPJResult:
    _correctness = data['correctness']
    _score = data.get('score', None)
    _message = data.get('message', None)
    _detail = data.get('detail', None)

    return _load_from_values(_correctness, _score, _message, _detail)


def _load_core_result_from_tuple(head) -> Tuple[bool, Optional[float]]:
    if isinstance(head, (list, tuple)):
        _correctness, _score = tuple(head)
    else:
        _correctness, _score = head, None

    return _correctness, _score


def _load_result_from_tuple(data: tuple) -> SPJResult:
    if not data:
        raise ValueError(
            'Tuple result should has no less than 1 object but {actual} found.'.format(actual=repr(len(data))))
    elif len(data) == 1:
        (_core,), _message, _detail = data, None, None
    elif len(data) == 2:
        (_core, _message), _detail = data, None
    elif len(data) == 3:
        _core, _message, _detail = data
    else:
        raise ValueError(
            'Tuple result should has no more than 3 object but {actual} found.'.format(actual=repr(len(data))))

    _correctness, _score = _load_core_result_from_tuple(_core)
    return _load_from_values(_correctness, _score, _message, _detail)


def _load_result_from_any_data(data) -> SPJResult:
    if isinstance(data, SimpleSPJResult):
        return data
    elif isinstance(data, ContinuitySPJResult):
        return data
    elif isinstance(data, dict):
        return _load_result_from_dict(data)
    elif isinstance(data, (list, tuple)):
        return _load_result_from_tuple(tuple(data))
    else:
        return SimpleSPJResult(not not data)


@enum_tools.documentation.document_enum
@int_enum_loads(name_preprocess=str.upper)
@unique
class ResultType(IntEnum):
    """
    Overview:
        Loading types of the result.
    """
    FREE = 0  # doc: Free mode. Just use the returned result.
    SIMPLE = 1  # doc: Simple mode. Convert the returned result to simple spj result.
    CONTINUITY = 2  # doc: Continuity mode. Conbert the returned result to continuity spj result.


def load_result(data, type_=None) -> SPJResult:
    """
    Overview:
        Load the given result data with result type's format.

    Arguments:
        - data: The given original result data.
        - type\_: The expected type. Default is ``None``, which means ``ResultType.FREE``.

    Returns:
        - result (:obj:`SPJResult`): Converted result object.
    """
    _result = _load_result_from_any_data(data)
    type_ = ResultType.loads(type_ or ResultType.FREE)
    if type_ == ResultType.SIMPLE:
        return to_simple(_result)
    elif type_ == ResultType.CONTINUITY:
        return to_continuity(_result)
    else:
        return _result


def to_simple(data) -> SimpleSPJResult:
    """
    Overview:
        Transform the given data to :class:`pyspj.models.simple.SimpleSPJResult` object.

    Arguments:
        - data: The given original data.

    Returns:
        - result (:obj:`SimpleSPJResult`): Converted result object.
    """
    return SimpleSPJResult(**load_result(data).to_json())


def to_continuity(data) -> ContinuitySPJResult:
    """
    Overview:
        Transform the given data to :class:`pyspj.models.simple.ContinuitySPJResult` object.

    Arguments:
        - data: The given original data.

    Returns:
        - result (:obj:`ContinuitySPJResult`): Converted result object.
    """
    _dict = dict(load_result(data).to_json())
    if 'score' not in _dict:
        _dict['score'] = 0.0
    return ContinuitySPJResult(**_dict)
