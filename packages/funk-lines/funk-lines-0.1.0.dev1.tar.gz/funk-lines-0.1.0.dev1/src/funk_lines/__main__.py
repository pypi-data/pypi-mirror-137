"""Entrypoint of the python package."""
from .cli import app

__all__ = ["app"]

# Execute the CLI app when calling the module via python -m funk-lines
if __name__ == "__main__":
    app()
