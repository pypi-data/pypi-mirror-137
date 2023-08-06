"""Base analyser from which all analysers inherit"""
import abc
import logging
import typing

from .. import results

logger = logging.getLogger(__name__)


class BaseAnalyser(abc.ABC):
    """Analyser ABC"""

    def __init__(self, location: typing.Any) -> None:
        self.location = location

    def analyse(self) -> results.BaseResult:
        """Executes the analysis"""
        try:
            return self._analyse()
        except Exception as err:
            logger.critical("Exception from %s", self.location)
            raise err

    @abc.abstractmethod
    def _analyse(self) -> results.BaseResult:
        """Abstract method for executing analyser"""
        raise NotImplementedError()
