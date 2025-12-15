from token import CIRCUMFLEXEQUAL
import asyncio
from functools import cache
from itertools import batched, permutations

from aoc.commons.linear_equations import LinearEquationsSystem

from .commons import AOC2025Day10, Button, Machine


class AOC2025Day10Part2(AOC2025Day10):
    verbose_output = True
    #answer = 0
    example_answer = 33
    skip_puzzle = True

    def solve(self):
        for instructions in self.read_input():
            machine = Machine(instructions)

            # Create eq systems 
            machine_code = machine.apply_science()
            self.log(machine_code)

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

            break
        # return asyncio.run(self.helping_the_elfes())

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

    async def charge_machine(self, machine_instructions: str) -> int:
        machine = Machine(machine_instructions)

        machine.run_bj2o()
        
        n_presses = max(machine.joltage.jolts_target)
        while True:
            if self.use_finger(machine, [0 for _ in range(machine.joltage.n_indicators)], n_presses):
                # Found solution
                return n_presses

            n_presses += 1
    
    def use_finger(self, machine: Machine, base_state: list[int], presses_remaining: int, button_to_press: int = 0) -> bool:
        button = machine.job[button_to_press]

        finger_endurance = sum([remaining_button.max_joltage_presses for remaining_button in machine.job[button_to_press:]])

        # 
        if presses_remaining > finger_endurance and button_to_press + 1 != len(machine.job):
            return False
        

        # Optimize the min and max time to press the button based on current state and number of presses still allowed by the remaining buttons
        min_range, max_range = button.optimize_presses(machine.joltage.jolts_target, base_state, finger_endurance)
        if presses_remaining < min_range:
            return False
        
        max_range = min(presses_remaining + 1, max_range)

        # self.log(f"From {base_state}, pressing {button}. Estimated range is {press_range} with a remaining endurance of {finger_endurance}.")

        for n_presses in range(min_range, max_range):
            new_state = machine.joltage.charge(base_state, button.buttons, n_presses)
                
            # self.log(f"Reached new state {new_state} with {n_presses} presses of {button}.")
            # We reached the joltage target, return the number of times we pressed this button to the previous loop
            if new_state == machine.joltage.jolts_target:
                return True
            
            # if machine.overcharged()
            
            # Recursively test the other buttons
            if button_to_press + 1 < len(machine.job):
                pressed = self.use_finger(machine, new_state, presses_remaining - n_presses, button_to_press + 1)

                # One of the button down the line succesfully charged the machine
                if pressed:
                    return True
                
        
        # No solution found with the given state and allowed number of presses
        return False
            
