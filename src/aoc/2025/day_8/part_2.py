import re 

from aoc.core.puzzle import AOCPuzzle

class Circuit:
    x: float
    y: float
    z: float

    def __init__(self, position: str):
        position = re.sub(r"\s", "", position)
        self.position = position

        coordinates = position.split(",")
        self.x = int(coordinates[0])
        self.y = int(coordinates[1])
        self.z = int(coordinates[2])

    def distance(self, other_circuit: "Circuit") -> int:
        return (self.x - other_circuit.x)**2 + (self.y - other_circuit.y)**2 + (self.z - other_circuit.z)**2

    def __repr__(self):
        return f"x: {self.x} - y: {self.y} - z: {self.z}"


class AOC2025Day8Part1(AOCPuzzle):
    #verbose_output = True
    answer = 8361881885
    #example_answer = 40

    latest_circuit_id: int = 0
    plugged_circuits: dict

    def solve(self):
        input = self.input
        answer = 0

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

            n_circuits = len(list(set(list(self.plugged_circuits.values()))))
            self.log(f"Current number of circuits: {n_circuits}")
            if n_circuits == 1:
                break


        self.log(f"Final pair plugged: {new_pair}")

        return new_pair[0].x * new_pair[1].x

    def fetch_circuits_positions(self) -> list[Circuit]:
        circuits = []
        for coordinates in self.read_input():
            circuits.append(Circuit(coordinates))

        self.log(f"Found {len(circuits)} circuits")
        return circuits


    def find_circuits_distances(
        self, 
        circuits: list[Circuit],
    ) -> tuple[list[int], tuple[Circuit, Circuit]]:

        distances = []
        circuits_pairs = {}

        for i in range(0, len(circuits)):
            for j in range (i + 1, len(circuits)):
                distance = circuits[i].distance(circuits[j])
                distances.append(distance)
                circuits_pairs[distance] = (circuits[i], circuits[j])

        distances.sort()
        return distances, circuits_pairs

    def plug_circuits(self, circuits_pair: tuple[Circuit, Circuit]):
        circuit_a = None
        circuit_a_position = circuits_pair[0].position
        if circuit_a_position in self.plugged_circuits:
            circuit_a = self.plugged_circuits[circuit_a_position]

        circuit_b = None
        circuit_b_position = circuits_pair[1].position
        if circuit_b_position in self.plugged_circuits:
            circuit_b = self.plugged_circuits[circuit_b_position]

        if circuit_a is None and circuit_b is None:
            self.latest_circuit_id += 1
            self.plugged_circuits[circuit_a_position] = self.latest_circuit_id
            self.plugged_circuits[circuit_b_position] = self.latest_circuit_id
            return

        if circuit_b is None:
            self.plugged_circuits[circuit_b_position] = circuit_a
            return
        if circuit_a is None:
            self.plugged_circuits[circuit_a_position] = circuit_b
            return

        if circuit_a == circuit_b:
            return
        
        self.replace_circuits_ids(circuit_a, circuit_b)

    def replace_circuits_ids(self, circuit_a, circuit_b):
        plugged_circuits = self.plugged_circuits
        for circuit, id in plugged_circuits.items():
            if id != circuit_b:
                continue
            self.plugged_circuits[circuit] = circuit_a

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

