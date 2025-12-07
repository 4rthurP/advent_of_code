from aoc.core.puzzle import AOCPuzzle


class AOC2025Day1Part1(AOCPuzzle):
    answer = 995
    example_answer = 3

    def solve(self):
        answer = 0
        counter = 50
        for line in self.input_path.open("r"):
            amount = int(line[1 : len(line)]) % 100
            if amount > 100:
                raise ValueError(f"Amount must be between 1 and 100: {amount}")

            match line[0]:
                case "R":
                    counter += amount
                case "L":
                    counter -= amount
                case _:
                    raise ValueError(f"Unexpected character {line[0]} in {line}")

            if counter < 0:
                counter = 100 + counter
            elif counter >= 100:
                counter = counter - 100

            if counter == 0:
                answer += 1

        return answer
