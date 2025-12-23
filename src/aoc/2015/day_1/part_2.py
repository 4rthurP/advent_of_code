import re

from .commons import AOC2025Day1


class AOC2025Day1Part1(AOC2025Day1):
    answer = 1797
    example_answer = None

    def solve(self):
        input = re.sub(r"\s", "", self.input)
        answer = 0

        for pos, char in enumerate(input):
            match(char):
                case "(":
                    answer += 1
                case ")":
                    answer -= 1
                case _:
                    self.log(f"Unknown char: {char}")

            if answer == -1:
                return pos + 1

        return None
