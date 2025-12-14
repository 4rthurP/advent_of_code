from re import L
import time
import sys
from polars.selectors import enum


class LinearEquationsSystem:
    starting_systems: list[list[float]]
    current_form: list[list[float]]
    row_echelon_form: list[list[float]]
    reduced_form: list[list[float]]

    solutions: list[float]

    solve_time: float

    def __init__(
        self,
        coefficients: list[list[float]],
        unknowns: list[float] | None = None,
    ):
        self.is_solved = False
        if unknowns is not None:
            if len(unknowns) != len(coefficients):
                raise ValueError(
                    f"The number of unknowns {len(unknowns)} given is not equal to the number of systems ({len(coefficients)})."
                )
            for i, u in enum(unknowns):
                coefficients[i][len(coefficients)] = u

        self.starting_systems = coefficients
        self.check_shape()

    def __repr__(self):
        repr = f"System of {self.n} equations"
        if self.is_solved:
            repr += f" solved in {self.solve_time:.4f}s: {self.solutions}"

    @property
    def n(self):
        return len(self.starting_systems)
    
    def check_shape(self):
        for system in self.starting_systems:
            if len(system) != self.n + 1:
                raise ValueError(f"System should be of length {self.n + 1}, {len(system)} given.")
            
    def solve_system(self) -> list[float]:
        start_time = time.time()
        self.order()
        self.shape()
        self.reduce()

        self.solutions = []
        for system in self.reduced_form:
            self.solutions.append(system[self.n])

        self.solve_time = time.time() - start_time
        self.is_solved = True
        return self.solutions

    @property
    def is_echelonned(self):
        for i in range(0, self.n):
            if self.current_form[i][i]:
                return False

        return True

    def shape(self):
        "Recursively shapes the matrix toward a row echelon"
        col = 0
        last_system = []
        systems = self.current_form

        for row in range(0, self.n):
            system = systems[row]
            # Find the next pivot column
            if system[col] == 0:
                col += 1
            for inner_row in range(row, self.n + 1):
                # Next system is already reduced
                if systems[inner_row][col] == 0:
                    continue

                # Reduce the biggest system and order systems with smallest on top
                system, new_system = self._reduce_system(col, systems[inner_row], system)
                systems[row] == system
                systems[inner_row] = new_system

        self.current_form = systems
        if not self.is_echelonned:
            self.order()
            self.shape()

    def _reduce_system(self, col: int, current_system: list[int], previous_system: list[int]) -> tuple[list[int], list[int]]:
        if current_system[col] < previous_system[col]:
            small_system = current_system
            big_system = previous_system
        else:
            small_system = previous_system
            big_system = current_system

        if big_system[col] % small_system[col] != 0:
            return small_system, big_system

        factor = big_system[col] / small_system[col]

        new_system = []
        for i in range(0, len(current_system)):
            new_system[i] = big_system[i] - factor * small_system[i]

        return small_system, big_system


    def reduce(self):
        pass
