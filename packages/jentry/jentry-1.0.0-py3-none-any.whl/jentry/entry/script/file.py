import codecs
from typing import Iterator, Tuple

import javalang
from javalang.ast import Node
from javalang.tree import MethodDeclaration, PackageDeclaration, ClassDeclaration

from ...model import JavaEntry


def is_entry_method(node: Node) -> bool:
    """
    Determine if the given method node is an entry or not.

    :param node: Given method node.
    :return: Valid or not.
    """
    if 'public' in node.modifiers and 'static' in node.modifiers \
            and node.name == 'main' and node.return_type is None and len(node.parameters) == 1:
        param = node.parameters[0]
        if param.name == 'args' and param.type.name == 'String' and (
                (not param.varargs and param.type.dimensions == [None]) or
                (param.varargs and param.type.dimensions == [])
        ):
            return True

    return False


def load_entries_from_file(filename: str) -> Iterator[JavaEntry]:
    """
    Load entries from one java source code file.

    :param filename: File name.
    :return: Iterator of :class:`jentry.model.entry.JavaEntry` objects.
    """
    with codecs.open(filename, 'r') as cf:
        for package, clazz in load_entry_classes_from_code(cf.read()):
            yield JavaEntry(filename, package, clazz)


def load_entry_classes_from_code(code: str) -> Iterator[Tuple[str, str]]:
    """
    Load entry classes from one java source code.

    :param code: Java source code string.
    :return: Iterator of entry class tuples.
    """
    parsed_code = javalang.parse.parse(code)

    package = None
    for pkgpath, pkgnode in parsed_code.filter(PackageDeclaration):
        if isinstance(pkgnode, PackageDeclaration):
            package = pkgnode.name

    for clspath, clsnode in parsed_code.filter(ClassDeclaration):
        if len(clspath) == 2 and 'private' not in clsnode.modifiers:
            is_entry = False
            for mthpath, mthnode in clsnode.filter(MethodDeclaration):
                if len(mthpath) == 2 and is_entry_method(mthnode):
                    is_entry = True
                    break

            if is_entry:
                yield package, clsnode.name
