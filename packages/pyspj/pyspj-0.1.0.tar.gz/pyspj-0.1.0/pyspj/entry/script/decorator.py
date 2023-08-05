import codecs
import io
from functools import wraps


def stdin_string_support(func):
    @wraps(func)
    def _func(stdin, **kwargs):
        if isinstance(stdin, str):
            with io.StringIO(stdin) as stdin_stream:
                return func(stdin=stdin_stream, **kwargs)
        else:
            return func(stdin=stdin, **kwargs)

    return _func


def stdout_string_support(func):
    @wraps(func)
    def _func(stdout, **kwargs):
        if isinstance(stdout, str):
            with io.StringIO(stdout) as stdout_stream:
                return func(stdout=stdout_stream, **kwargs)
        else:
            return func(stdout=stdout, **kwargs)

    return _func


def string_support(func):
    return stdin_string_support(stdout_string_support(func))


def stdin_file_trans(func):
    @wraps(func)
    def _func(stdin, **kwargs):
        with codecs.open(stdin, 'r') as stdin_file:
            return func(stdin=stdin_file, **kwargs)

    return _func


def stdout_file_trans(func):
    @wraps(func)
    def _func(stdout, **kwargs):
        with codecs.open(stdout, 'r') as stdout_file:
            return func(stdout=stdout_file, **kwargs)

    return _func


def file_trans(func):
    return stdin_file_trans(stdout_file_trans(func))
