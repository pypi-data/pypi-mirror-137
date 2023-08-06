"""Code of the main entrypoint for the application"""
import os
import pathlib

from . import results
from .analysers import dir_analyser, file_analyser


def main(path: os.PathLike[str] | str) -> results.BaseResult:
    """Runs funk_lines against a file or directory"""
    path_ = pathlib.Path(path)

    if not path_.exists():
        raise FileNotFoundError(str(path))

    if path_.is_dir():
        result = dir_analyser.DirectoryAnalyser(path).analyse()
    else:
        result = file_analyser.FileAnalyser(path).analyse()

    return result
