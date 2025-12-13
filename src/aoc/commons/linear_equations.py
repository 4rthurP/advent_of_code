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
    
    def order(self):
        current_shape = []


    def reshape(self)
        "Order by number of leading zeros."
        order = {}
        for line in self.current_form:
            leading_zeros = 0
            for n in line:
                if n != 0:
                    break
                leading_zeros += 1
            if leading_zeros not in order:
                order[leading_zeros] = []
            order[leading_zeros].append(line)

        self.current_form = [*order]
                

                
        pass

    def reduce(self):
        pass
