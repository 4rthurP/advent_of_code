from aoc.core.puzzle import AOCPuzzle


class AOC2025DayXPartX(AOCPuzzle):
    # verbose_output = True
    answer = 9173

    def solve(self):
        answer = 0
        n_moves = 0
        input = self.input
        lines = input.split("\n")

        while True:
            n_moves += 1
            movable_rolls = 0
            new_lines = []
            for i in range(0, len(lines)):
                moved_rolls, moved_line = self.check_line(i, lines)
                movable_rolls += moved_rolls
                new_lines.append(moved_line)

            self.log(f"Found {movable_rolls} rolls in turn {n_moves}.")
            answer += movable_rolls
            if movable_rolls == 0:
                break
            # Reset lines to new arrangement
            lines = new_lines
        self.log(f"Took {n_moves} - Final drawing")
        
        for line in lines:
            self.log(line, 30)
        return answer
    
    def check_line(self, i: int, lines: list[str]) -> tuple[int, str]:
        line = lines[i]
        moved_line = lines[i]

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
                moved_line = moved_line[:place] + "." + moved_line[place + 1:] 
            
        return movable_rolls, moved_line
    
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
            

            

