from .commons import AOC2025Day8


class AOC2025Day8Part1(AOC2025Day8):
    # verbose_output = True
    answer = 8361881885
    example_answer = 25272

    def solve(self):
        circuits = self.fetch_circuits_positions()
        distances, pairs = self.find_circuits_distances(circuits)

        self.latest_circuit_id = 0
        self.plugged_circuits = {}

        n_pair = 0
        while True:
            current_pair_distance = distances[n_pair]
            new_pair = pairs[current_pair_distance]
            self.plug_circuits(new_pair)
            n_pair += 1

            # While not all circuits are plugged, continue
            if len(self.plugged_circuits) < 1000:
                continue

            n_circuits = len(list(set(self.plugged_circuits.values())))
            self.log(f"Current number of circuits: {n_circuits}")
            if n_circuits == 1:
                break

        self.log(f"Final pair plugged: {new_pair}")

        return new_pair[0].x * new_pair[1].x
