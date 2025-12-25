from .commons import AOC2025Day2


class AOC2025Day2Part2(AOC2025Day2):
    answer = 3783758

    def solve(self):
        answer = 0
        for line in self.read_input():
            l, w, h = line.split("x")
            side_1 = 2 * int(l)
            side_2 = 2 * int(w)
            side_3 = 2 * int(h)

            answer += int(l) * int(w) * int(h)
            answer += min(side_1 + side_2, side_2 + side_3, side_3 + side_1)

        return int(answer)
