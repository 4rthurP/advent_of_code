from aoc.core.puzzle import AOCPuzzle


class AOC2025Day3Part1(AOCPuzzle):
    answer = 169935154100102
    def solve(self):
        answer = 0

        for line in self.read_input():
            answer += self.get_line_answer(line, 12)

        return answer
    
    def get_line_answer(self, line: str, target_lenght: int):
        line = line.strip()

        answer = []
        current_line = line

        while len(answer) != target_lenght:
            max_num = 0
            max_pos = 0
            
            for pos, number in enumerate(current_line):
                if int(number) > max_num:
                    max_num = int(number)
                    max_pos = pos
                if len(current_line) - pos == target_lenght - len(answer):
                    break
            answer.append(str(max_num))
            current_line = current_line[max_pos+1:]

        self.log(f"Found max joltage {''.join(answer)} for line {line}")

        if len(answer) != target_lenght:
            raise ValueError(f"Incorrect lenght for line {line}: {answer} ({len(answer)})")

        return int("".join(answer))
