"""Class for analysing a directory"""
import os
import pathlib

from funk_lines.core import results

from . import base_analyser, file_analyser


class DirectoryAnalyser(base_analyser.BaseAnalyser):
    """Analyser for directories"""

    def __init__(self, dir_path: str | os.PathLike[str]):
        """
        Args:
            dir_path: Location to the file to be analysed
        """
        self._dir_path: pathlib.Path = pathlib.Path(str(dir_path))
        if not self._dir_path.is_dir():
            raise NotADirectoryError(dir_path)

    def analyse(self) -> results.BaseResult:
        """Extracts the results from the analysed object.

        Returns:
            Results object
        """
        results_list: list[results.BaseResult] = []
        for path in self._dir_path.iterdir():
            if path.is_dir():
                result = DirectoryAnalyser(path).analyse()
                if not isinstance(result, results.EmptyResult):
                    results_list.append(result)
            elif path.is_file() and path.suffix == ".py":
                result = file_analyser.FileAnalyser(path).analyse()
                results_list.append(result)

        result = sum(results_list, start=results.EmptyResult(name="EMPTY"))
        result.name = str(self._dir_path)
        if len(results_list) > 1:
            result.children = results_list
        return result
