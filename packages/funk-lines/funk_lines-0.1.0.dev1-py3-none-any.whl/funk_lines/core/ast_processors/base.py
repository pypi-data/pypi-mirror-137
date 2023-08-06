"""Base classes and objects for processing AST trees."""
import ast
import logging

logger: logging.Logger = logging.getLogger(__name__)


class EOF(ast.stmt):
    """AST object to signal the end-of-file."""

    name: str = "EOF"

    def __init__(self, lineno: int):
        """Constructor for EOF.

        Args:
            lineno: line number
        """
        super().__init__()
        self.lineno: int = lineno


class StmtInfo:
    """Class for extracting important information on functions and classes."""

    def __init__(
        self,
        current_node: ast.stmt,
        next_node: ast.stmt,
    ):
        """Constructor for Definition info.

        Args:
            current_node: AST node of the function or class
            next_node: AST node of the following object
        """
        self._current_node: ast.stmt = current_node
        self._next_node: ast.stmt | None = next_node

        self._line_start: int = self._current_node.lineno

        self._line_end: int = self._next_node.lineno - 1
        self._n_lines: int = self._line_end - self._line_start + 1

        logger.debug("Catch stmt %s", self)

    @property
    def n_lines(self) -> int:
        """Number of lines."""
        return self._n_lines


AstFlowControl = (ast.While, ast.For, ast.AsyncFor, ast.If, ast.Try)
AstDefinitions = (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)
