import sys
from multiprocessing import Value
from re import S
import asyncio
from itertools import batched

from .commons import AOC2025Day10, Machine


class AOC2025Day10Part2(AOC2025Day10):
    verbose_output = True
    #answer = 0
    example_answer = 33
    # skip_puzzle = True

    def solve(self):
        for instructions in self.read_input():
            asyncio.run(self.use_finger(instructions))
            # break
        # return asyncio.run(self.helping_the_elfes())

    async def reduce_systems(self, systems: list[list[float]]):
        "Recursively shapes the matrix toward a row echelon"

        for row in range(0, len(systems)):
            system = systems[row]
            for inner_row in range(row + 1, len(systems)):
                # Next system is already reduced
                # if systems[inner_row][col] == 0:
                #     continue

                # Reduce the biggest system and order systems with smallest on top
                self.log(f"Reducing {system} with {systems[inner_row]}")
                system, new_system = await self._reduce( systems[inner_row], system)
                self.log(f"Result: {system}, {new_system}")
                systems[row] = system
                systems[inner_row] = new_system

            self.log(systems)
            # Find the next pivot column

        return systems

    async def _reduce(self, system_a: list[float], system_b: list[float]):
        small_system = None
        big_system = None

        # Find the system to keep at the top and the one to reduce
        first_non_zero = None
        for col in range(0, len(system_a) - 1):
            if first_non_zero is None and (system_a[col] != 0 or system_b[col] != 0):
                first_non_zero = col
            if system_a[col] == system_b[col]:
                continue
            if abs(system_a[col]) < abs(system_b[col]):
                small_system = system_a
                big_system = system_b
                break

            small_system = system_b
            big_system = system_a
            break

        if small_system is None or big_system is None:
            if system_a[len(system_a) - 1] != system_b[len(system_a) -1] :
                raise ValueError(f"No solution for {system_a} and {system_b}")
            self.log(f"[red]Found two equal systems: {system_a}, {system_b}[/red]")
            return system_a, system_b

        # No reduction is needed, simply return the ordered systems
        if first_non_zero is None or small_system[first_non_zero] == 0:
            self.log(f"No reduction needed for {small_system}")
            return big_system, small_system
        factor = small_system[first_non_zero] / big_system[first_non_zero]
        
        self.log(f"Col: {first_non_zero} - factor: {factor}")

        new_system = [
            small_system[i] - factor * big_system[i]
            for i in range(0, len(system_a))
        ]
        return big_system, new_system

    async def back_substitue(self, systems: list[list[float]]):
        non_free_variables = []
        solutions = []

        for row in reversed(systems):
            # Find the first non 0 in the row
            col = None
            coef = 1
            has_solution = True
            for i, k in enumerate(row):
                if k == 0:
                    continue

                # Reduce to 1x and find if we know the solution or not
                if col is None:
                    col = i 
                    coef = row[i]
                else:
                    has_solution = False
                row[i] = row[i] / coef
            
            # We have an empty row
            if col is None:
                raise ValueError(f"Found empty row: {row}")
                continue
            
            non_free_variables.append(col)
                    
            if not has_solution:
                self.log(f"No solution for {row}")
                solutions.append(None)
                continue

            solution = row[len(row) - 1]
            solutions.append(solution)

            # Substitute the solution in all lines above
            for m in range(0, col):
                if systems[m][col] == 0:
                    continue

                coef = systems[m][col]
                systems[m][len(row) - 1] = systems[m][len(row) - 1] - systems[m][col] * solution
            
        # Deduce the free variables from the ones we used in the substitution
        free_variables = [col for col in range(0, len(systems[0])) if col not in non_free_variables]
        self.log(f"Finished back substitution: {systems} with free variables {free_variables} and solutions {solutions}")
        return systems, free_variables, solutions
                    

    async def helping_the_elfes(self) -> int:
        n_pushes = 0
        for batch in batched(self.read_input(), 50, strict=False):
            pushes = await asyncio.gather(
                *[
                    self.charge_machine(machine_instructions)
                    for machine_instructions in batch
                ]
            )
            n_pushes += sum(pushes)

        return n_pushes

    async def use_finger(self, instructions: str):
        machine = Machine(instructions)

        # Create eq systems 
        machine_code = machine.apply_science()
        self.log(f"Machine code: {machine_code}")

        echelon_form = await self.reduce_systems(machine_code)
        final_form, free_variables, solutions = await self.back_substitue(echelon_form)

        if len(free_variables) == 0:
            raise ValueError(f"Yay no free variables: {final_form}")

        # Reduce to echelon form
            # ???

        # Back substitute

        # Loop through systems to 
        # - find free variables (replace line by 0 ?)
        # - find solved unknowns

        # If solved return solution
        # If one free variable ???

        # For each free variables
        # Express other variables in terms of free variables (n column matrixes) and find min/max
        # Loop through remaining possibilities starting from 0 and stop when one is found
        # Look for the smallest solution between all free variable

        # Return result


