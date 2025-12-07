from aoc.core.puzzle import AOCPuzzle


class AOC2025Day7Part1(AOCPuzzle):
    #verbose_output = True
    answer = 1672
    example_answer = 21

    def solve(self):
        input = self.input
        #self.log(input)

        beam_splits = 0 # Count number of splits
        current_line = -1 # Count current line to pass odd ones where nothing happens

        for stage in self.read_input():
            current_line += 1
            if current_line == 0:
                beams_positions = [len(stage) // 2 - 1] # Keep track of all beams
                self.log(f"Beam position in first line: {beams_positions} - {stage[beams_positions[0]]}")
                continue

            if current_line % 2 == 0:
                new_beams = []
                for beam_position in beams_positions:
                    if stage[beam_position] == "^":
                        # Beam is split in two
                        new_beams.extend(
                                [
                                    beam_position - 1,
                                    beam_position + 1,
                                ]
                            )
                        beam_splits += 1
                    else:
                        # Otherwise the beam continues at his current place
                        new_beams.append(beam_position)
                beams_positions = list(set(new_beams))

            if self.verbose_output:
                graph = stage
                for beam_position in beams_positions:
                    graph = graph[:beam_position] + "|" + graph[beam_position + 1:]
                self.log(graph)
                self.log(f"Current number of splits: {beam_splits}")

        return beam_splits
