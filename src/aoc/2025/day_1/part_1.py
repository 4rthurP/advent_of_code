from rich.console import Console

from aoc.core.puzzle import AOCPuzzle


class AOC2025Day1Part1(AOCPuzzle):
    def solve(self):
        console = Console()
        input = self.input
        console.print(input)

        return 1