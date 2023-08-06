import os
from typing import List, Iterator

import click
from click.core import Context, Option

from .format import DEFAULT_ENTRY_FORMAT, EntryFormat
from .order import DEFAULT_SORT_ORDER, SortOrder
from ..script import load_entries_from_file, load_entries_from_project
from ...config.meta import __TITLE__, __VERSION__, __AUTHOR__, __AUTHOR_EMAIL__
from ...model import JavaEntry


# noinspection DuplicatedCode,PyUnusedLocal
def print_version(ctx: Context, param: Option, value: bool) -> None:
    """
    Print version information of cli.

    :param ctx: click context
    :param param: current parameter's metadata
    :param value: value of current parameter
    """
    if not value or ctx.resilient_parsing:
        return  # pragma: no cover
    click.echo('{title}, version {version}.'.format(title=__TITLE__.capitalize(), version=__VERSION__))
    click.echo('Developed by {author}, {email}.'.format(author=__AUTHOR__, email=__AUTHOR_EMAIL__))
    ctx.exit()


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


def _click_load_entries(paths: List[str]) -> Iterator[JavaEntry]:
    for path in paths:
        if os.path.exists(path):
            if os.path.isfile(path):
                yield from load_entries_from_file(path)
            else:
                yield from load_entries_from_project(path)
        else:
            raise click.FileError(f'File not found - {repr(path)}.')  # pragma: no cover


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False, is_eager=True,
              help="Show package's version information.")
@click.option('-f', '--format', 'format_',
              type=click.types.Choice(list(map(str.lower, EntryFormat.__members__.keys()))),
              default=DEFAULT_ENTRY_FORMAT.name.lower(), show_default=True,
              help="The format to display the entries")
@click.option('-s', '--sorted_by',
              type=click.types.Choice(list(map(str.lower, SortOrder.__members__.keys()))),
              default=DEFAULT_SORT_ORDER.name.lower(), show_default=True,
              help='The order to sorted by.')
@click.option('-r', '--reverse', is_flag=True, default=False, show_default=True,
              help='Reverse the sorted result, only applied when -s is used.')
@click.option('-F', '--first_only', type=bool, is_flag=True, default=False, show_default=True,
              help="Only show the first entry.")
@click.argument('sources', nargs=-1, type=click.types.Path(exists=True, readable=True))
def cli(format_, sorted_by, reverse, first_only, sources):
    """
    Jentry - find the entry of your java project.
    """
    format_ = EntryFormat.loads(format_)
    sorted_by = SortOrder.loads(sorted_by)
    reverse = not not reverse

    entries = sorted(_click_load_entries(sources), key=sorted_by.order_func, reverse=reverse)
    if first_only:
        if entries:
            format_.print_first_entry(entries[0])
        else:
            raise click.ClickException(f'No entry found in {repr(sources)}.')
    else:
        format_.print_entries(entries)
