"""Base analyser from which all analysers inherit"""
import abc

from .. import results


class BaseAnalyser(abc.ABC):
    """Analyser ABC"""

    @abc.abstractmethod
    def analyse(self) -> results.BaseResult:
        """Abstract method for executing analyser"""
        raise NotImplementedError()
