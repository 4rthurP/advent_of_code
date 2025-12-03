from aoc.core.puzzle import AOCPuzzle


class AOC2025Day3Part1(AOCPuzzle):
    answer = 17142
    def solve(self):
        answer = 0

        for line in self.read_input():
            answer += self.get_line_answer(line)

        return answer
    
    def get_line_answer(self, line: str):
        max_num = (0, 0)
        min_num = (0, 0)

        line = line.strip()

        for place, number in enumerate(line):
            try:
                number = int(number)
            except ValueError:
                continue

            if number > max_num[0]:
                min_num = (0, 0) if place != len(line) - 1 else max_num
                max_num = (number, place)
                    
            elif number > min_num[0]:
                min_num = (number, place)
        
        line_anwser = f"{max_num[0]}{min_num[0]}" if min_num[1] > max_num[1] else f"{min_num[0]}{max_num[0]}"
        self.log(f"Found max joltage {line_anwser} for line {line}")

        return int(line_anwser)
