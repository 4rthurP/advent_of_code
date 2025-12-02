from aoc.core.puzzle import AOCPuzzle


class AOC2025Day1Part2(AOCPuzzle):
    answer = 5847

    def solve(self):
        answer = 0
        counter = 50
        for line in self.input_path.open("r"):
            amount = int(line[1 : len(line)])

            while amount > 0:
                if counter == 0 and amount >= 100:
                    answer += 1
                    amount -= 100
                    continue

                if line[0] == "R":
                    rotation = min(100 - counter, amount)
                    counter += rotation
                    if counter == 100:
                        counter = 0
                else:
                    if counter == 0:
                        counter = 100
                        rotation = amount
                    else:
                        rotation = min(counter, amount)
                    counter -= rotation

                if counter == 0:
                    answer += 1

                amount -= rotation
        return answer
