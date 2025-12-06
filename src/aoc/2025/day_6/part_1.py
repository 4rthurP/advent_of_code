import re

from aoc.core.puzzle import AOCPuzzle

class AOC2025Day6Part1(AOCPuzzle):
    #verbose_output = True
    answer = 5782351442566

    def solve(self):
        input = self.input
        answer = 0

        input_lines = input.replace("\n\n", "\n").split("\n")

        lines = []
        for line in input_lines:
            lines.append(re.sub('\s+', ' ', line).split(" "))

        for op in range(0, len(lines[0])):
            if lines[4][op] == "+":
                answer += int(lines[0][op]) + int(lines[1][op]) + int(lines[2][op]) + int(lines[3][op])
            else:
                answer += int(lines[0][op]) * int(lines[1][op]) * int(lines[2][op]) * int(lines[3][op])
                



        return answer
