from platform import python_version
from typing import Optional

import click
from click.core import Context, Option

from .base import CONTEXT_SETTINGS, _DEFAULT_RESULT_TYPE, run_test
from ...config.meta import __TITLE__, __VERSION__
from ...models import ResultType


def pyspj_entry(name: str, spj, result_type: str = _DEFAULT_RESULT_TYPE,
                version: Optional[str] = None, author: Optional[str] = None, email: Optional[str] = None):
    """
    Create your pyspj CLI entry.

    :param name: Name of the special judge.
    :param spj: Special judge function or string.
    :param result_type: Type of result, default is ``FREE``.
    :param version: Version information, default is ``None``.
    :param author: Author of this special judge, default is ``None``.
    :param email: Author email of this special judge, default is ``None``.
    :return: A click function, can be used directly to create a CLI program.
    """
    result_type = ResultType.loads(result_type)

    def print_version(ctx: Context, param: Option, value: bool) -> None:
        if not value or ctx.resilient_parsing:
            return
        if version:
            click.echo(f'Special judge - {name}, version {version}.')
        else:
            click.echo(f'Special judge - {name}.')
        if author:
            if email:
                click.echo(f'Developed by {author}, {email}.')
            else:
                click.echo(f'Developed by {author}.')
        click.echo(f'Powered by {__TITLE__}, version {__VERSION__}.')
        click.echo(f'Based on Python {python_version()}.')
        ctx.exit()

    @click.command(context_settings=CONTEXT_SETTINGS,
                   help=f"{name.capitalize()} - test a pair of given input and output.")
    @click.option('-v', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True,
                  help="Show special judge's version information.")
    @click.option('-i', '--input', 'input_content', type=str, help='Input content of special judge.')
    @click.option('-o', '--output', 'output_content', type=str, help='Output content of special judge')
    @click.option('-I', '--input_file', type=click.Path(exists=True, dir_okay=False, readable=True),
                  help='Input file of special judge (if -i is given, this will be ignored).')
    @click.option('-O', '--output_file', type=click.Path(exists=True, dir_okay=False, readable=True),
                  help='Output file of special judge (if -o is given, this will be ignored).')
    @click.option('-V', '--value', type=str, multiple=True,
                  help='Attached values for special judge (do not named as "stdin" or "stdout").')
    @click.option('-p', '--pretty', type=bool, is_flag=True,
                  help='Use pretty mode to print json result.')
    def _built_cli(input_content, output_content,
                   input_file, output_file, value, pretty):
        return run_test(input_content, output_content, input_file, output_file, value, result_type, spj, pretty)

    return _built_cli
