import re

from .commons import AOC2025Day1


class AOC2025Day1Part1(AOC2025Day1):
    answer = 280
    example_answer = None

    def solve(self):
        input = re.sub(r"\s", "", self.input)
        down = len(input.replace("(", ""))
        return len(input) - (2 * down)
