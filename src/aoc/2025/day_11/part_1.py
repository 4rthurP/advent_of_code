import re

from .commons import AOC2025Day11


class AOC2025Day11Part1(AOC2025Day11):
    verbose_output = True
    answer = 470
    example_answer = 5
    devices: dict[str, list[str]]

    def solve(self):
        self.devices = {}
        for line in self.read_input():
            instructions = re.sub(r"\n", "", line).split(": ")
            self.devices[instructions[0]] = [dev for dev in instructions[1].split(" ")]

        return self.count_outward_paths("you")

    def count_outward_paths(self, current_device: str) -> int:
        paths_count = 0
        if current_device not in self.devices:
            raise ValueError(f"Unknown device {current_device}")

        for output in self.devices[current_device]:
            if output == "out":
                paths_count += 1
                continue

            paths_count += self.count_outward_paths(output)

        return paths_count

