from .commons import AOC2025Day8


class AOC2025Day8Part1(AOC2025Day8):
    # verbose_output = True
    answer = 244188
    example_answer = 40

    def solve(self):
        circuits = self.fetch_circuits_positions()
        distances, pairs = self.find_circuits_distances(circuits)

        self.latest_circuit_id = 0
        self.plugged_circuits = {}

        for n_pair in range(0, 1000):
            current_pair_distance = distances[n_pair]
            new_pair = pairs[current_pair_distance]
            self.plug_circuits(new_pair)

        self.log(self.plugged_circuits)

        n_plugs = self.count_plugs()
        self.log(f"Final plugs count: {n_plugs}")

        return n_plugs[0] * n_plugs[1] * n_plugs[2]

    def count_plugs(self):
        counts = {}
        for circuit_id in self.plugged_circuits.values():
            if circuit_id in counts:
                counts[circuit_id] += 1
                continue
            counts[circuit_id] = 1

        counts = list(counts.values())
        counts.sort(reverse=True)

        return counts
