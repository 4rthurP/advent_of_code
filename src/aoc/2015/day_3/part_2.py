from .commons import AOC2015Day3


class AOC2015Day3Part2(AOC2015Day3):
    answer = 2360
    example_answer = None

    def solve(self):
        example_answer = None

        santa_pos = (0, 0)
        robot_pos = (0, 0)

        visited_houses = {
            0: {0: 1}
        }
        houses_with_gifts = 1

        for n, char in enumerate(self.input.strip()):
            if n % 2 == 0:
                x = santa_pos[0]
                y = santa_pos[1]
            else:
                x = robot_pos[0]
                y = robot_pos[1]

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

            if n % 2 == 0:
                santa_pos = (x, y)
            else:
                robot_pos = (x, y)

        self.log(f"Visited {houses_with_gifts} distinct houses which received gifts")

        return houses_with_gifts
