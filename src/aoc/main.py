"""Main CLI entry point for AoC."""

import os
from typing import Annotated

import typer
from rich.console import Console

from aoc.core.day import AOCDay

console = Console()

app = typer.Typer(
    name="teapot",
    help="A CLI tool for package installation and configuration management",
    add_completion=False,
)


@app.command("aoc")
def aoc(
    day: Annotated[int | None, typer.Argument(help="Day of the AoC puzzle")],
    *,
    year: Annotated[
        int | None, typer.Option("--year", "-y", help="Year of the AoC puzzle")
    ] = None,
) -> None:
    """Run the given AOC puzzle."""
    aoc = AOCDay(day, year)
    if not aoc.is_ready:
        console.print(f"[red]❌ {aoc.error_msg}[/red]")

    aoc.solve()


@app.callback()
def main(
    *,
    verbose: Annotated[
        int,
        typer.Option(
            "--verbose",
            "-v",
            count=True,
            help="Enable verbose output (-v, -vv, -vvv for increasing detail)",
        ),
    ] = 0,
) -> None:
    """AOC CLI - Advent of Code Python CLI."""
    if verbose > 0:
        level_names = ["", "basic", "detailed", "debug"]
        level_name = level_names[min(verbose, 3)]
        typer.echo(f"Verbose mode enabled (level {verbose} - {level_name})")
        # Store verbosity level in a way that command modules can access it
        os.environ["AOC_VERBOSITY"] = str(verbose)


if __name__ == "__main__":
    app()
