import math
import re

from aoc.core.puzzle import AOCPuzzle


class AOC2025Day6Part2(AOCPuzzle):
    #verbose_output = True
    answer = 10194584711842
    example_answer = 3263827

    def solve(self):
        input = self.input
        input_lines = input.split("\n")
        input_lines.pop() #Remove last trailing space
        operators = input_lines[4]

        answer = 0
        numbers = []
        result = 0
        operator = ""
        for col in range(0, len(input_lines[0])):
            current_num = ""
            for row in range(0, 4):
                digit = input_lines[row][col]
                if digit != " ":
                    current_num += digit

            if current_num == "":
                continue


            # First column of each problem contains the operator
            if operators[col] != " ":
                self.log(f"Result ({operator}): {result}")
                answer += result

                operator = operators[col]
                result = int(current_num)
            else:
                if operator == "+":
                    result += int(current_num)
                else:
                    result *= int(current_num)
            self.log(f"Current number: {current_num}")

        return answer + result
