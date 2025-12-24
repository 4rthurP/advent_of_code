import logging
import os
import time
from enum import StrEnum
from pathlib import Path

from rich.console import Console


class PuzzleState(StrEnum):
    NOT_STARTED = "not_started"
    UNKNOWN = "unknown"
    SOLVED = "solved"
    SOLVED_EXAMPLE = "solved example"
    FAILED = "failed"
    FAILED_EXAMPLE = "failed example"


class AOCPuzzle:
    year: int
    day: int
    part: int
    error_message: str
    solve_message: str = "Puzzle solved !"
    state: PuzzleState
    timer: int | None = None
    verbose_output: bool = False
    skip_puzzle: bool = False # Activate to only solve the exemple, useful for debugging
    solving_puzzle: bool = False
    solving_example: bool = False

    # Puzzle answer
    answer: any | None = None
    given_answer: any | None = None
    # Example answer
    example_answer: any | None = None
    given_example_answer: any | None = None

    def __init__(self, year: int, day: int, part: int):
        self.year = year
        self.day = day
        self.part = part

        self.input_value = None
        inputs_folder = (
            Path(__file__).parent.parent
            / str(self.year)
            / "inputs"
        )
        self.input_path = inputs_folder / f"day_{self.day}.txt"
        self.input_example_path = inputs_folder / f"day_{self.day}_example.txt"

        self.define_logger()

    @property
    def input(self):
        if self.input_value is None:
            self.input_value = self.input_path.read_text(encoding="utf-8")

        return self.input_value

    @property
    def has_input(self):
        return self.input_path.exists()
    
    def read_input(self):
        return self.input_path.open("r")

    def solve_puzzle(self):
        self.log("------------------------------------")
        self.log(f"Started solving Part {self.part} of Day {self.day} {self.year}")
        self.timer = 0

        # Solve main puzzle
        if not self.skip_puzzle:
            self.solving_puzzle = True
            timer_start = time.time()
            self.given_answer = self.solve()
            self.timer = time.time() - timer_start

            self.log(f"Puzzle solved in {self.timer:.4f}s")
            self.solving_puzzle = False

        # Switch input to solve example if the real answer has not been found yet
        if self.answer is None and self.example_answer is not None:
            self.solving_example = True
            # Even though the input property could handle the "solving_example" property, 
            # switching the input path directly allows to use this property directly in the puzzle without having to worry about the switch
            self.input_path = self.input_example_path 
            self.input_value = None # Reset the previous value loaded by the puzzle solving

            # Solve the puzzle using the example input
            self.given_example_answer = self.solve()
            self.solving_example = False

        self.check_answer()

        return self.state

    def solve(self) -> any:
        pass

    def check_answer(self):
        if self.answer is None:
            if self.example_answer is not None:
                if self.given_example_answer == self.example_answer:
                    self.state = PuzzleState.SOLVED_EXAMPLE
                    return
                self.state = PuzzleState.FAILED_EXAMPLE
                return
            self.state = PuzzleState.UNKNOWN
            return
        if self.answer == self.given_answer:
            self.state = PuzzleState.SOLVED
            return
        self.state = PuzzleState.FAILED

    def define_logger(self):
        # Create a logger specific to this class
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

        # Prevent propagation to root logger (optional)
        self.logger.propagate = False

        # Create file handler for this class
        log_file = (
            Path(__file__).parent.parent
            / str(self.year)
            / "logs"
            / f"day_{self.day}.txt"
        )
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        # Add handler to logger (check if already added to avoid duplicates)
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)

        # Also create a console to be used by the object
        self.console = Console()

    def log(self, msg: str, level: int = logging.INFO):
        if self.verbose_output or level >= 30:
            self.console.print(msg)
        self.logger.log(level, msg)
