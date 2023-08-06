import json
from enum import IntEnum, unique
from typing import List

import click
import enum_tools
from hbutils.model import int_enum_loads
from prettytable import PrettyTable

from ...model import JavaEntry


@enum_tools.documentation.document_enum
@int_enum_loads(enable_int=False, name_preprocess=str.upper)
@unique
class EntryFormat(IntEnum):
    TABLE = 1  # doc: Print in table format.
    JSON = 2  # doc: Print in pretty JSON format.
    ENTRY = 3  # doc: Print in simple java entry format.

    def print_first_entry(self, entry: JavaEntry):
        """
        Print the first given java entry object.

        :param entry: Given java entry object.
        :raises ValueError: Raise :class:`ValueError` when self is invalid.
        """
        if self == EntryFormat.TABLE:
            t = PrettyTable(['Item', 'Content'])
            t.add_row(['Entry', entry.full_name])
            t.add_row(['Package', entry.package if entry.package else '<none>'])
            t.add_row(['Class', entry.clazz])
            t.add_row(['Filename', entry.filename if entry.filename else '<none>'])
            click.echo(t)
        elif self == EntryFormat.JSON:
            click.echo(json.dumps({
                'entrance': entry.full_name,
                'package': entry.package,
                'class': entry.clazz,
                'file': entry.filename,
            }, indent=4))
        elif self == EntryFormat.ENTRY:
            click.echo(entry.full_name)
        else:
            raise ValueError(f'Unknown entry format - {repr(self)}.')  # pragma: no cover

    def print_entries(self, entries: List[JavaEntry]):
        """
        Print the given java entry objects.

        :param entries: Given java entries.
        :raises ValueError: Raise :class:`ValueError` when self is invalid.
        """
        if self == EntryFormat.TABLE:
            t = PrettyTable(['Entry', 'Package', 'Class', 'Filename'])
            for entry in entries:
                t.add_row([
                    entry.full_name,
                    entry.package if entry.package else '<none>',
                    entry.clazz,
                    entry.filename if entry.filename else '<none>'
                ])
            click.echo(t)
        elif self == EntryFormat.JSON:
            click.echo(json.dumps([{
                'entrance': entry.full_name,
                'package': entry.package,
                'class': entry.clazz,
                'file': entry.filename,
            } for entry in entries], indent=4))
        elif self == EntryFormat.ENTRY:
            for entry in entries:
                click.echo(entry.full_name)
        else:
            raise ValueError(f'Unknown entry format - {repr(self)}.')  # pragma: no cover


DEFAULT_ENTRY_FORMAT = EntryFormat.ENTRY
