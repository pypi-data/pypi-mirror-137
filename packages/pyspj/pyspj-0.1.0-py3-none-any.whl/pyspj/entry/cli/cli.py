from typing import Optional, List

import click
from click.core import Context, Option

from .base import CONTEXT_SETTINGS, run_test, _RESULT_TYPES, _DEFAULT_RESULT_TYPE
from ...config.meta import __TITLE__, __VERSION__, __AUTHOR__, __AUTHOR_EMAIL__


# noinspection PyUnusedLocal
def print_version(ctx: Context, param: Option, value: bool) -> None:
    """
    Print version information of cli.

    :param ctx: click context
    :param param: current parameter's metadata
    :param value: value of current parameter
    """
    if not value or ctx.resilient_parsing:
        return
    click.echo('{title}, version {version}.'.format(title=__TITLE__.capitalize(), version=__VERSION__))
    click.echo('Developed by {author}, {email}.'.format(author=__AUTHOR__, email=__AUTHOR_EMAIL__))
    ctx.exit()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False, is_eager=True,
              help="Show package's version information.")
@click.option('-i', '--input', 'input_content', type=str, help='Input content of special judge.')
@click.option('-o', '--output', 'output_content', type=str, help='Output content of special judge')
@click.option('-I', '--input_file', type=click.Path(exists=True, dir_okay=False, readable=True),
              help='Input file of special judge (if -i is given, this will be ignored).')
@click.option('-O', '--output_file', type=click.Path(exists=True, dir_okay=False, readable=True),
              help='Output file of special judge (if -o is given, this will be ignored).')
@click.option('-V', '--value', type=str, multiple=True,
              help='Attached values for special judge (do not named as "stdin" or "stdout").')
@click.option('-t', '--type', 'result_type',
              type=click.Choice(_RESULT_TYPES),
              help='Type of the final result.', default=_DEFAULT_RESULT_TYPE, show_default=True)
@click.option('-s', '--spj', type=str, required=True,
              help='Special judge script to be used.')
@click.option('-p', '--pretty', type=bool, is_flag=True,
              help='Use pretty mode to print json result.')
def cli(input_content: Optional[str], output_content: Optional[str],
        input_file: Optional[str], output_file: Optional[str],
        value: List[str], result_type: str, spj: str, pretty: bool):
    """
    Command line entry of pyspj CLI.

    :param input_content: Input content, should be a string or ``None``.
    :param output_content: Output content, should be a string or ``None``.
    :param input_file: Input filename, should be a string or ``None``.
    :param output_file: Output filename, should be a string or ``None``.
    :param value: Additional arguments, like ``KEY=VALUE``.
    :param result_type: Result type, should be a string.
    :param spj: Special judge string.
    :param pretty: Enable pretty print or not, default is on.
    """
    return run_test(input_content, output_content, input_file, output_file, value, result_type, spj, pretty)
