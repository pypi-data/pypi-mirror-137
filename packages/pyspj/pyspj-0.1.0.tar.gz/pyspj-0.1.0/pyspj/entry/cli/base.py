import json

from .exception import _raise_exception_with_exit_code
from .values import _load_from_values
from ..script import execute_spj
from ..script.decorator import stdin_string_support, stdin_file_trans, stdout_string_support, stdout_file_trans
from ...models.general import ResultType

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)

_RESULT_TYPES = {item.lower() for item in ResultType.__members__.keys()}
_DEFAULT_RESULT_TYPE = ResultType.FREE.name.lower()


def run_test(input_content, output_content,
             input_file, output_file, value, result_type,
             spj, pretty):
    if not input_content and not input_file:
        _raise_exception_with_exit_code(1, 'Either -i or -I should be given.')
    if not output_content and not output_file:
        _raise_exception_with_exit_code(1, 'Either -o or -O should be given.')

    _execute_func = execute_spj
    if input_content:
        _execute_func = stdin_string_support(_execute_func)
        _input = input_content
    else:
        _execute_func = stdin_file_trans(_execute_func)
        _input = input_file

    if output_content:
        _execute_func = stdout_string_support(_execute_func)
        _output = output_content
    else:
        _execute_func = stdout_file_trans(_execute_func)
        _output = output_file

    result_type = ResultType.loads(result_type)
    result = _execute_func(
        spj=spj, type_=result_type,
        stdin=_input, stdout=_output,
        arguments=_load_from_values(list(value)),
    )

    print(json.dumps(result.to_json(), indent=4 if pretty else None, sort_keys=True))
