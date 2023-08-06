"""Processes for functions and classes in AST trees."""
import ast
import functools
import itertools
from typing import Any, Iterable, Iterator, TypeVar

from .base import AstDefinitions, StmtInfo

T = TypeVar("T")


def _pairwise(iterable: Iterable[T], ending: T) -> Iterator[tuple[T, T]]:
    """Iterates through an object pairwise.

    Examples:
        s -> (s_0,s_1), (s_1,s_2), (s_2, s_3), ..., (s_last, ending)

    Args:
        iterable: Original iterable
        ending: Last value to after at ending

    Returns:
        Iterator of tuples of pairs
    """
    iterator_1, iterator_2 = itertools.tee(iterable)
    next(iterator_2, None)
    return itertools.zip_longest(iterator_1, iterator_2, fillvalue=ending)


def is_definition(node: Any) -> bool:
    """Returns True if the object is a definition ast node.

    Args:
        node: object to be evaluated

    Returns:
        True if node is a Definition
    """
    return any(isinstance(node, t) for t in AstDefinitions)


def get_definitions(
    current_node: ast.stmt | ast.Module,
    next_node: ast.stmt,
) -> "list[StmtInfo]":
    """Constructs a InfoSequence object from an AST node.

    Args:
        current_node: AST Node from which to generate the InfoSequence
        next_node: Next AST node, useful for extracting additional information

    Returns:
        List of StmtInfo
    """
    current_node_info: "list[StmtInfo]" = []

    if is_definition(current_node) and not isinstance(current_node, ast.Module):
        current_node_info = [StmtInfo(current_node, next_node=next_node)]

    if hasattr(current_node, "body"):
        _body: list[ast.stmt] = current_node.body  # type: ignore[union-attr]
        return functools.reduce(
            list.__add__,
            itertools.starmap(get_definitions, _pairwise(_body, ending=next_node)),
            current_node_info,
        )

    return current_node_info
