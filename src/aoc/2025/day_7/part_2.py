from aoc.core.puzzle import AOCPuzzle


class AOC2025Day7Part2(AOCPuzzle):
    # verbose_output = True
    answer = 231229866702355
    example_answer = 40

    def solve(self):
        input = self.input
        current_line = -1 # Count current line to pass odd ones where nothing happens
        beams_positions = {} # Keep track of all beams

        for stage in self.read_input():
            current_line += 1
            if current_line == 0:
                position = len(stage) // 2 - 1
                beams_positions = {position: 1}
                continue

            if current_line % 2 == 1:
                continue

            new_beams = {}
            for beam_position in list(beams_positions.keys()):
                if stage[beam_position] == "^":
                    # Beam is split in two
                    new_positions = [
                        beam_position - 1,
                        beam_position + 1,
                    ]
                else:
                    # Otherwise the beam continues at his current place
                    new_positions = [beam_position]

                for position in new_positions:
                    if position in new_beams:
                        new_beams[position] += beams_positions[beam_position]
                    else:
                        new_beams[position] = beams_positions[beam_position]
            beams_positions = new_beams
        self.log(f"Beams positions: {beams_positions}")
        n_beams = 0
        for pos in list(beams_positions.keys()):
            n_beams += beams_positions[pos]

        return n_beams
