import io
import sys
import traceback
from functools import wraps

from .decorator import string_support, file_trans
from .imports import _load_func
from ...models import load_result, SPJResult


def _spj_preprocess(spj):
    """
    Process spj to be safe.

    :param spj: Original special judge function.
    :return: Processed special judge function.
    """
    spj = _load_func(spj)

    @wraps(spj)
    def _func(*args, **kwargs):
        try:
            return spj(*args, **kwargs)
        except Exception as err:
            with io.StringIO() as eis:
                traceback.print_exception(*sys.exc_info(), file=eis)
                err_info = eis.getvalue()

            return False, 'Exception occurred while special judge - {cls}.'.format(cls=repr(err)), err_info

    return _func


def execute_spj(spj, stdin, stdout, type_=None, arguments=None) -> SPJResult:
    """
    Execute the special judge.

    :param spj: Special judge function, can be a string or a spj-function.
    :param stdin: Stdin stream, can be a string stream or a file stream.
    :param stdout: Stdout stream, should be a string stream or a file stream.
    :param type_: Load type, should be a result mode string or enum.
    :param arguments: Attached arguments.
    :return: Result of this special judge.
    """
    return load_result(_spj_preprocess(spj)(stdin=stdin, stdout=stdout, **(arguments or {})), type_)


def execute_spj_from_string(spj, stdin, stdout, type_=None, arguments=None) -> SPJResult:
    """
    Execute special judge with string value.

    :param spj: Special judge function, can be a string or a spj-function.
    :param stdin: Stdin stream, can be a string stream.
    :param stdout: Stdout stream, should be a string stream.
    :param type_: Load type, should be a result mode string or enum.
    :param arguments: Attached arguments.
    :return: Result of this special judge.
    """
    return execute_spj(string_support(_spj_preprocess(spj)), stdin, stdout, type_, arguments)


def execute_spj_from_file(spj, stdin_file, stdout_file, type_=None, arguments=None) -> SPJResult:
    """
    Execute special judge with string file.

    :param spj: Special judge function, can be a string or a spj-function.
    :param stdin_file: Stdin stream, can be a file stream.
    :param stdout_file: Stdout stream, should be a file stream.
    :param type_: Load type, should be a result mode string or enum.
    :param arguments: Attached arguments.
    :return: Result of this special judge.
    """
    return execute_spj(file_trans(_spj_preprocess(spj)), stdin_file, stdout_file, type_, arguments)
