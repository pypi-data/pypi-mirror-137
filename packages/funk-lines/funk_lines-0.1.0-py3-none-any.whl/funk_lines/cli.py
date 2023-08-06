"""Command-line interface."""
import pathlib
import typing

import rich.console
import rich.table
import typer
from rich import box

if typing.TYPE_CHECKING:
    from funk_lines.core.results import BaseResult


app: typer.Typer = typer.Typer(name="Funk Lines CLI")
console = rich.console.Console()

NAME_INDENT = 4


def _version_callback(value: bool) -> None:
    if value:
        import pkg_resources

        version = pkg_resources.get_distribution(__name__.split(".", maxsplit=1)[0]).version

        console.print(f"Funk Lines [cyan]{version}[/cyan]")
        raise typer.Exit(code=0)


def __add_result_to_table(table: rich.table.Table, result: "BaseResult", level: int = 0) -> None:
    table.add_row(" " * level * NAME_INDENT + result.name, *result.info())
    for child in result.children:
        __add_result_to_table(table, child, level + 1)


@app.command()
def callback(
    version: bool = typer.Option(
        False, "--version", callback=_version_callback, help="Show version and exit.", is_eager=True
    ),
    src: pathlib.Path = typer.Argument(..., dir_okay=True, file_okay=True, exists=True),
) -> None:
    """Funk Lines CLI."""
    from .core import main, results

    _ = version

    result = main.main(src)

    if isinstance(result, results.EmptyResult):
        console.print(f"[bold]{src}[/bold] does not contain any python files", style="red")
        raise typer.Exit(code=1)

    table = rich.table.Table(
        rich.table.Column("Name", justify="left", style="cyan", no_wrap=True),
        rich.table.Column("Lines", justify="right", style="magenta"),
        rich.table.Column("Functions", justify="right", style="magenta"),
        rich.table.Column("Lines/Func", justify="right", style="green"),
        show_edge=False,
        show_header=True,
        expand=False,
        box=box.SIMPLE,
    )

    __add_result_to_table(table, result)

    console.print(table)
