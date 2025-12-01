import os
from enum import StrEnum
from pathlib import Path


class PuzzleState(StrEnum):
    NOT_STARTED = "not_started"
    UNKNOWN = "unknown"
    SOLVED = "solved"
    FAILED = "failed"


class AOCPuzzle:
    year: int
    day: int
    part: int
    error_message: str
    solve_message: str = "Puzzle solved !"
    state: PuzzleState
    answer: any | None = None
    given_answer: any | None = None

    def __init__(self, year: int , day: int , part: int):
        self.year = year or os.environ["CURRENT_YEAR"]
        self.day = day
        self.part = part

        self.input_value = None
        self.input_path = Path(__file__).parent.parent / str(self.year) / "inputs" / f"day_{self.day}_part_{self.part}.txt"

    @property
    def input(self):
        if self.input_value is None:
            self.input_value = self.input_path.read_text(encoding="utf-8")

        return self.input_value
    
    @property
    def has_input(self):
        return self.input_path.exists()

    def solve_puzzle(self):
        self.given_answer = self.solve()
        self.check_answer()
        return self.state

    def solve(self) -> any:
        pass

    def check_answer(self):
        if self.answer is None:
            self.state = PuzzleState.UNKNOWN
            return
        if self.answer == self.given_answer:
            self.state = PuzzleState.SOLVED
            return
        self.state = PuzzleState.FAILED
