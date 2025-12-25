from .commons import AOC2015Day3


class AOC2015Day3Part1(AOC2015Day3):
    answer = 2592
    example_answer = None

    def solve(self):
        x = 0
        y = 0

        visited_houses = {
            0: {0: 1}
        }
        houses_with_gifts = 1

        for char in self.input.strip():
            match(char):
                case ">":
                    x += 1
                case "<":
                    x -= 1
                case "^":
                    y += 1
                case "v":
                    y -= 1
                case _:
                    raise ValueError(f"Invalid character: {char}")

            if x not in visited_houses:
                visited_houses[x] = {}
            if y not in visited_houses[x]:
                visited_houses[x][y] = 1
                houses_with_gifts += 1
            else:
                visited_houses[x][y] += 1

        self.log(f"Visited {houses_with_gifts} distinct houses which received gifts")

        return houses_with_gifts
