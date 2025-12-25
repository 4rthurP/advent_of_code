from .commons import AOC2025Day2


class AOC2025Day2Part1(AOC2025Day2):
    answer = 1588178

    def solve(self):
        answer = 0
        for line in self.read_input():
            l, w, h = line.split("x")
            side_1 = 2 * int(l) * int(w)
            side_2 = 2 * int(w) * int(h)
            side_3 = 2 * int(h) * int(l)

            answer += (side_1 + side_2 + side_3)
            answer += min(side_1, side_2, side_3) / 2

        return int(answer)
