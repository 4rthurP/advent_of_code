from weakref import ref
import sys
from multiprocessing import Value
from re import S
import asyncio
from itertools import batched

from .commons import AOC2025Day10, Machine, System

class AOC2025Day10Part2(AOC2025Day10):
    verbose_output = True
    #answer = 0
    example_answer = 33
    # skip_puzzle = True

    def solve(self):
        self.freedom_counter = 0
        for instructions in self.read_input():
            asyncio.run(self.use_finger(instructions))
            # break
        # return asyncio.run(self.helping_the_elfes())

    async def reduce_systems(self, systems: list[System]):
        "Recursively shapes the matrix toward a row echelon"

        for row in range(0, len(systems)):
            system = systems[row]
            for inner_row in range(row + 1, len(systems)):
                # Next system is already reduced
                # if systems[inner_row][col] == 0:
                #     continue

                # Reduce the biggest system and order systems with smallest on top
                # self.log(f"Reducing {system} with {systems[inner_row]}")
                system, new_system = await self._reduce( systems[inner_row], system)
                # self.log(f"Result: {system}, {new_system}")
                systems[row] = system
                systems[inner_row] = new_system

            # self.log(systems)
            # Find the next pivot column

        return systems

    async def _reduce(self, system_a: System, system_b: System) -> tuple[System, System]:
        if system_b.non_leading_zero is None:
            return system_a, system_b
        if system_a.non_leading_zero is None:
            return system_b, system_a

        small_system = system_b
        big_system = system_a
        # Find the system to keep at the top and the one to reduce
        for col in range(0, len(system_a) - 1):
            if system_a[col] == system_b[col]:
                continue
            if (abs(system_a[col]) < abs(system_b[col]) or system_b[col] == 0) and system_a[col] != 0:
                break

            small_system = system_a
            big_system = system_b
            break

        # No reduction is needed, simply return the ordered systems
        if small_system[big_system.non_leading_zero] == 0:
            # self.log(f"No reduction needed for {small_system}")
            return big_system, small_system
        
        self.log(f"Reduving {small_system} with {big_system}")
        small_system.reduce(big_system)
        self.log(f"Results in {small_system}")
        return big_system, small_system
        
    def _reduce_rows(self, reference_col: int, reference_system: list[float], system_to_reduce: list[float]) -> list[float]:
        factor = system_to_reduce[reference_col] / reference_system[reference_col]
        
        return [
            system_to_reduce[i] - factor * reference_system[i]
            for i in range(0, len(reference_system))
        ]

    async def back_substitute(self, systems: list[System]):
        for i, reference in enumerate(systems):
            # Empty systems
            if reference.non_leading_zero is None:
                continue
            for system in systems[:i]:
                if system[reference.non_leading_zero] == 0:
                    continue
                system.reduce(reference)

        return systems


        # for row in reversed(systems):
        #     # Find the first non 0 in the row
        #     col = None
        #     coef = 1
        #     has_solution = True
        #     for i, k in enumerate(row[:len(row) - 1]):
        #         if k == 0:
        #             continue

        #         # Reduce to 1x and find if we know the solution or not
        #         if col is None:
        #             col = i 
        #             coef = row[i]
        #         else:
        #             # Found a second column with a non-zero factor
        #             has_solution = False
        #         # TODO: see if we need the reduction of not
        #         row[i] = row[i] / coef
            
        #     # We have an empty row
        #     if col is None:
        #         continue
            
        #     non_free_variables.append(col)
                    
        #     if not has_solution:
        #         self.log(row)
        #         solutions.append(None)
        #         continue

        #     solution = row[len(row) - 1] / row[col]
        #     solutions.append(solution)

        #     # Substitute the solution in all lines above
        #     for m in range(0, min(col, len(systems))):
        #         if systems[m][col] == 0:
        #             continue
                
        #         systems[m][col] = 0
        #         systems[m][len(row) - 1] = systems[m][len(row) - 1] - systems[m][col] * solution
            
        # # Deduce the free variables from the ones we used in the substitution
        # free_variables = [col for col in range(0, len(systems[0]) - 1) if col not in non_free_variables]
        # self.log(f"Finished back substitution: {systems} with free variables {free_variables} and solutions {solutions}")
        # return systems, free_variables, solutions
                    

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
        self.log(f"Echelon form: {echelon_form}")
        final_form = await self.back_substitute(echelon_form)

        self.log(f"Final form: {final_form}")

        

        # If solved return solution
        # If one free variable ???

        # For each free variables
        # Express other variables in terms of free variables (n column matrixes) and find min/max
        
        # Loop through systems to 
        # - find free variables (replace line by 0 ?)
        # - find solved unknowns

        # Loop through remaining possibilities starting from 0 and stop when one is found
        # Look for the smallest solution between all free variable

        # Return result


