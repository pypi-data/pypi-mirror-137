"""File for the results class."""
import abc
import operator
import statistics
from typing import Sequence

from .ast_processors import StmtInfo


class BaseResult(abc.ABC):
    """Abstract base class for other results"""

    def __init__(self, name: str, children: "list[BaseResult] | None" = None):
        """
        Args:
            name: string detailing the origin of the result
        """
        self.name = name
        self.children: "list[BaseResult]" = children or []
        self.children.sort(key=operator.attrgetter("name"))

    def __str__(self) -> str:
        return f"Result from {self.name}"

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.name})"

    @abc.abstractmethod
    def __add__(self, other: "BaseResult") -> "BaseResult":
        raise NotImplementedError()

    @property
    def total_lines(self) -> int:
        """Total number of lines."""
        return 0

    @property
    def nbr_definitions(self) -> int:
        """Total number of functions and classes."""
        return 0

    @property
    def definitions(self) -> list[StmtInfo]:
        """List of statement info objects for all functions and classes."""
        return []

    @property
    def lines_per_function(self) -> float | None:
        """Mean number of lines per definition."""
        return None

    def info(self) -> tuple[str, str, str]:
        """Returns the information of the result in a printable manner"""
        return (
            str(self.total_lines),
            str(self.nbr_definitions),
            f"{self.lines_per_function:.2f}" if self.lines_per_function else "",
        )


class EmptyResult(BaseResult):
    """Empty result, used for aggregating with other results"""

    def __add__(self, other: "BaseResult") -> "BaseResult":
        """Adding an empty result with a result returns the simple result"""
        return other


class Result(BaseResult):
    """Class for holding the results of an analysis.

    The Analyser classes return a Result object.
    """

    def __init__(
        self,
        total_lines: int,
        definitions: Sequence[StmtInfo],
        name: str,
        children: list[BaseResult] | None = None,
    ):
        """
        Args:
            total_lines: Total number of lines
            definitions: Sequence of functions and classes
            name: details the origin of the result
        """
        self._total_lines: int = total_lines
        self._definitions: list[StmtInfo] = list(definitions)
        super().__init__(name=name, children=children)

    @property
    def total_lines(self) -> int:
        """Total number of lines."""
        return self._total_lines

    @property
    def nbr_definitions(self) -> int:
        """Total number of functions and classes."""
        return len(self._definitions)

    @property
    def definitions(self) -> list[StmtInfo]:
        """List of statement info objects for all functions and classes."""
        return self._definitions.copy()

    @property
    def lines_per_function(self) -> float | None:
        """Mean number of lines per definition."""
        if self._definitions:
            return statistics.mean(def_.n_lines for def_ in self._definitions)
        return None

    def __add__(self, other: "BaseResult") -> "BaseResult":
        """Combines two results.

        Args:
            other: another Result object

        Returns:
            Combined results
        """
        return self.__class__(
            total_lines=self.total_lines + other.total_lines,
            definitions=self._definitions + other.definitions,
            name=f"Combined {self.name} + {other.name}",
        )
