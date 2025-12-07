from aoc.core.puzzle import AOCPuzzle


class AOC2025DayXPartX(AOCPuzzle):
    # verbose_output = True
    answer = 1626
    example_answer = 13

    def solve(self):
        answer = 0
        input = self.input
        lines = input.split("\n")
        for i in range(0, len(lines)):
            n_valid = self.check_line(i, lines)
            self.log(f"Found {n_valid} rolls in line {i + 1}")
            answer += n_valid


        return answer
    
    def check_line(self, i: int, lines: list[str]) -> int:
        line = lines[i]

        lines_to_check = [
            lines[i - 1] if i > 0 else None,
            line,
            lines[i + 1] if i < len(lines) - 1 else None
        ]

        movable_rolls = 0

        #Find all rolls
        for place, item in enumerate(line):
            #Check a roll when found
            if item == "@" and self.check_roll(place, lines_to_check):
                movable_rolls += 1
                
            
        return movable_rolls
    
    def check_roll(self, place: int, lines: list[str]) -> bool:
        n_rolls = 0
        for i in range(0, 3):
            col = i - 1
            for j in range(0, 3):
                row = j - 1
                line = lines[j]

                #First and last row have empty neighbours
                if line is None:
                    continue

                #Handle items at each end of the row
                if col + place < 0 or col + place >= len(line):
                    continue

                # The roll of interest does not count
                if col == 0 and row == 0:
                    continue

                if line[col + place] == "@":
                    n_rolls += 1
                if n_rolls >= 4:
                    return False
                
        return True
            

            

