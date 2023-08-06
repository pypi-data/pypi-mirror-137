"""Core package for processing an AST tree."""
from .base import EOF, StmtInfo
from .function_processor import get_definitions

__all__ = ["EOF", "StmtInfo", "get_definitions"]
