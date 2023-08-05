from typing import Optional, Mapping

from hbutils.model import get_repr_info
from hbutils.string import truncate

from .base import SPJResult


def _check_score(score: float) -> float:
    score = float(score)
    if score < 0:
        raise ValueError('Score value should be no less than 0 but {actual} found.'.format(actual=repr(score)))
    elif score > 1:
        raise ValueError('Score value should be no greater than 1 but {actual} found.'.format(actual=repr(score)))

    return score


class ContinuitySPJResult(SPJResult):
    """
    Overview:
        Result of continuity special judge.
    """

    def __init__(self, correctness: bool, score: float,
                 message: Optional[str] = None, detail: Optional[str] = None, **kwargs):
        """
        Constructor for :class:`pyspj.models.continuity.ContinuitySPJResult`.

        :param correctness: correctness of result
        :param score: score of result
        :param message: message of result
        :param detail: detail of result
        """
        SPJResult.__init__(self, correctness, message, detail, **kwargs)
        self.__score = _check_score(score)

    @property
    def score(self) -> float:
        """
        Score of this result.
        """
        return self.__score

    def to_json(self) -> Mapping[str, str]:
        return {
            **SPJResult.to_json(self),
            'score': self.score,
        }

    def __repr__(self):
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('correctness', lambda: repr(self.correctness)),
                ('score', lambda: '%.3f' % self.score),
                ('message', lambda: truncate(repr(self.message), width=64, tail_length=16, show_length=True)),
            ]
        )

    def _tuple(self):
        _correctness, _message, _detail = SPJResult._tuple(self)
        return _correctness, self.__score, _message, _detail
