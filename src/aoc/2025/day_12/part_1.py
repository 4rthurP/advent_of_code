import re
import copy
import time

from .commons import AOC2025Day12
from functools import cache


class Present:
    id: int
    line_size: int = 3
    orientations: set
    line_size: int
    size: int


    def __init__(self, instruction_set: str):
        instructions = instruction_set.split(":\n")
        self.id = int(instructions[0])
        self.draw_shape(instructions[1])

        def assess_size(self, shape: tuple[int]):
            self.size = sum(shape)

    def draw_shape(self, shape: str):
        # self.line_size = len(shape.split("\n")[0])
        raw_shape = re.sub(r"\s", "", shape)
        self.shape = tuple([1 if char is "#" else 0 for char in raw_shape])

        self.size = sum(self.shape)

class Tree:
    width: int
    height: int
    size: int
    requested_presents: list[Present]
    presents_size: int = 0

    def __init__(self, santa_letter: str, presents: dict[str, Present]):
        requirements = santa_letter.split(": ")
        area = requirements[0].split("x")
        self.width = int(area[0]) 
        self.height = int(area[1])
        self.size = self.width * self.height

        self.requested_presents = []
        for id, n_presents in enumerate(requirements[1].split(" ")):
            present = presents[str(id)]
            self.requested_presents.extend([present] * int(n_presents))
            self.presents_size += present.size * int(n_presents)

    def __repr__(self):
        return f"Tree of size {self.width} by {self.height} ({self.size} s.u.) with {len(self.requested_presents)} presents needed ({self.presents_size} s.u.)."

    def can_hold_all_presents(self):
        if self.size < self.presents_size:
            return False
        return True

    def can_fit_all_presents(self):
        "Test is all presents can simply fit by being placed side-by-side"
        usable_width = self.width - (self.width % 3)
        usable_height = self.height - (self.height % 3)
        if usable_width * usable_height < len(self.requested_presents) * 9:
            return False
        return True

class AOC2025Day12Part1(AOC2025Day12):
    verbose_output = True
    answer = 408
    example_answer = None

    def solve(self):

        presents = {}
        christmas_trees = []
        for line in self.input.split("\n\n"):
            if line[1] == ":":
                presents[line[0]] = Present(line)
                continue

            for tree_design in line.split("\n"):
                if tree_design == "":
                    break
                christmas_trees.append(Tree(tree_design, presents))

        stats = {
            "too_small": 0,
            "big_enough": 0,
            "total": 0,
        }
        answer = 0
        for tree in christmas_trees:
            stats["total"] += 1
            if not tree.can_hold_all_presents():
                stats["too_small"] += 1
                continue
            if tree.can_fit_all_presents():
                stats["big_enough"] += 1
                answer += 1
                continue
        self.log(f"Since there was no processing at all, here are some refreshing stats about these trees : {stats}")
        return answer
