import re

from .commons import AOC2025Day11
from functools import cache

class AOC2025Day11Part1(AOC2025Day11):
    verbose_output = True
    answer = 384151614084875
    example_answer = None # Example changed for part 2 TODO: add optional part 2 example input
    devices: dict[str, list[str]]

    def solve(self):
        self.devices = {}
        for line in self.read_input():
            instructions = re.sub(r"\n", "", line).split(": ")
            self.devices[instructions[0]] = [dev for dev in instructions[1].split(" ")]

        a = self.count_outward_paths("svr", ("fft", "out"), "dac")
        b = self.count_outward_paths("dac", ("svr", "out"), "fft")
        c = self.count_outward_paths("fft", ("dac", "svr"), "out")

        d = self.count_outward_paths("svr", ("dac", "out"), "fft")
        e = self.count_outward_paths("fft", ("svr", "out"), "dac")
        f = self.count_outward_paths("dac", ("fft", "svr"), "out")
        return a * b * c + d * e * f

    @cache
    def count_outward_paths(self, current_device: str, avoid_nodes: tuple[str], target_output: str) -> int:
        paths_count = 0
        if current_device in avoid_nodes:
            return 0

        for output in self.devices[current_device]:
            if output == target_output:
                paths_count += 1
                continue

            paths_count += self.count_outward_paths(output, avoid_nodes, target_output)

        return paths_count

