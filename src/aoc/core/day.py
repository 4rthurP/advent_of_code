import importlib
import inspect
import os

from rich.console import Console

from aoc.core.puzzle import AOCPuzzle, PuzzleState


class AOCDay:
    year: int
    day: int
    n_parts: int
    is_ready: bool
    puzzles: list[AOCPuzzle]
    error_msg: str | None = None


    def __init__(self, day: int, year: int | None = None, n_parts: int = 2):
        self.year = year or os.environ["CURRENT_YEAR"]
        self.day = day
        self.n_parts = n_parts
        self.is_ready = False

        self.load_puzzles()

    def error(self, msg: str):
        if self.error_msg is None:
            self.error_msg = msg

    def load_puzzles(self):
        self.puzzles = []
        for n in range(1, self.n_parts):
            loader_response, success = self._load_class(n)

            if not success:
                # Do not raise an error when further parts are not available as of now
                if len(self.puzzles) == 0:
                    self.error(loader_response)
                return 
            
            puzzle_class: AOCPuzzle = loader_response
            puzzle = puzzle_class(self.year, self.day, n)
            if not puzzle.has_input:
                self.error(f"Part {n} of day {self.day} is missing an input ({puzzle.input_path}).")
                return
            
            self.puzzles.append(puzzle)
        self.is_ready = True

    def solve(self):
        if not self.is_ready:
            return
        
        console = Console()
        console.print("---------------------------")
        console.print(f"Day {self.day} of {self.year}")
        for puzzle in self.puzzles:
            console.print(f"Solving part {puzzle.part} of {self.day}")
            puzzle.solve_puzzle()
            match(puzzle.state):
                case PuzzleState.UNKNOWN:
                    console.print(f"[yellow]Answer given for part {puzzle.part}: {puzzle.given_answer}[/yellow]")
                case PuzzleState.SOLVED:
                    console.print(f"[green]Correct ! {puzzle.given_answer} was the right answer for part {puzzle.part} ![/green]")
                case PuzzleState.FAILED:
                    console.print(f"[red]Unfortunatly, {puzzle.given_answer} is not the right answer for part {puzzle.part} ![/red]")
                case _:
                    console.print(f"[red]An unknown error happened while solving par {puzzle.part} ![/red]")
        return         
                

    def _load_class(self, part: str) -> tuple[AOCPuzzle, True] | tuple[str, False]:
        """
        Dynamically import and return a class if it exists.
            
        Args:
            module_path: The module path (e.g., 'myapp.handlers.user')
            class_name: The class name to import (e.g., 'UserHandler')
            
        Returns:
            The class if found, None otherwise
        """
        try:
            # Import the module
            module = importlib.import_module(f"{self.year}.day_{self.day}.part_{part}")
                
            classes = [
                cls for name, cls in inspect.getmembers(module, inspect.isclass)
                if cls.__module__ == module.__name__
            ]
                    
            return classes[0], True
                    
        except ModuleNotFoundError:
            return f"Class for Day {self.day} part {part} of {self.year} does not exist", False
        except Exception as e:
            return f"Error importing: {e}", False