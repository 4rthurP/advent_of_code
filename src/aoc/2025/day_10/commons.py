from multiprocessing import Value
import math
import re
from itertools import product
from math import floor, ceil
from typing import TYPE_CHECKING

from rich.console import Console

from aoc.commons.maths import is_almost_integral
from aoc.core.puzzle import AOCPuzzle

if TYPE_CHECKING:
    from collections.abc import Iterable


class System:
    system: list[float]
    non_leading_zero: int | None
    solution: int | None

    def __init__(self, system: list[float]):
        self.system = system
        self.solution = None
        self.find_non_leading_zero()

    def __repr__(self):
        return f"System {self.system}"

    def __getitem__(self, index: int):
        return self.system[index]

    def __setitem__(self, index: int, value: float):
        self.system[index] = value

    def __iter__(self):
        return iter(self.system)

    def __len__(self):
        return len(self.system)
    
    def __add__(self, value: float | System):
        if isinstance(value, System):
            self.system = [
                var + value[i] for i, var in enumerate(self.system)
            ]
            return self

        self.system = [
            var + value for var in self.system
        ]
        return self
    
    def __sub__(self, value: float | System):
        if isinstance(value, System):
            self.system = [
                var - value[i] for i, var in enumerate(self.system)
            ]
            return self

        self.system = [
            var - value for var in self.system
        ]
        return self
    
    def __mul__(self, value: float):
        self.system = [
            var * value for var in self.system
        ]
        return self

    @property
    def joltage(self):
        return self[-1]

    def set_solution(self, solution: int):
        self.solution = int(solution)

    def find_non_leading_zero(self):
        for col, n in enumerate(self.system):
            if n != 0:
                self.non_leading_zero = col
                return

        self.non_leading_zero = None

    def find_solution(self):
        # It's a free variable
        if self.non_leading_zero is None:
            return None

        # It depends on one of the free variables
        for n in range(self.non_leading_zero + 1, len(self.system) - 1):
            if not math.isclose(self[n], 0, abs_tol=0.01):
                return None

        # We can give a solution
        self.solution = self[-1] / self[self.non_leading_zero]
        return self.solution

    def reduce(self, reference: System):
        if reference.non_leading_zero is None:
            return
        factor = (
            self.system[reference.non_leading_zero]
            / reference[reference.non_leading_zero]
        )

        for i in range(0, len(reference)):
            self[i] -= factor * reference[i]

        self.find_non_leading_zero()

    def count_presses(self, free_variables_presses: dict[int, int]) -> int | None:
        if self.solution is not None:
            return self.solution

        if self.non_leading_zero is None:
            return 0

        total = self[-1]
        for variable in free_variables_presses:
            total -= self[variable] * free_variables_presses[variable]

        if total < 0:
            return None

        return total / self[self.non_leading_zero]


class Light:
    n: int
    target: list[bool]
    current_state: list[bool]

    def __init__(self, lights_instruction: str):
        self.n = len(lights_instruction)
        self.target = [char == "#" for char in lights_instruction]
        self.reset()

    def __repr__(self):
        if self.is_lit:
            return f"Lights are on !! {self.state}"
        return f"Lights target {self.target} - Lights state {self.current_state}"

    @property
    def is_lit(self):
        return self.current_state == self.target

    @property
    def state(self):
        lights_schema = ["#" if light else "." for light in self.current_state]
        return f"[{''.join(lights_schema)}]"

    def reset(self):
        self.current_state = [False for _ in range(self.n)]

    def switch_lights(self, buttons: list[int]):
        for press in buttons:
            self.current_state[press] = not self.current_state[press]


class Button:
    buttons: list[int]

    max_joltage_presses: int | None
    min_joltage_presses: int = 0

    is_free_variable: bool = True
    solution: int | None

    def __init__(self, button_instruction: str):
        self.buttons = [int(button) for button in button_instruction.split(",")]
        self.max_joltage_presses = None

    def __repr__(self):
        return f"Button targets {self.buttons}. !! Do not press more than {self.max_joltage_presses} times, machine breakage risk !!"

    @property
    def range(self):
        if self.max_joltage_presses is None:
            raise ValueError("Max presses is not set.")
        return range(int(self.min_joltage_presses), int(self.max_joltage_presses) + 1)

    @property
    def has_solution(self):
        return self.solution is not None

    def targets(self, position: int):
        return position in self.buttons

    def set_max_presses(self, n: int):
        "Keep the minimum value given to make sure a button is not pressed too many times."
        if n < 0:
            raise ValueError(n)
        if self.max_joltage_presses is None or n < self.max_joltage_presses:
            self.max_joltage_presses = n
        return

    def set_min_presses(self, n: int):
        if n <= self.min_joltage_presses:
            return
        self.min_joltage_presses = n

    def optimize_presses(
        self, jolts_target: list[int], current_state: list[int], finger_endurance: int
    ) -> tuple[int, int]:
        biggest_press = 0
        max_press: int = self.max_joltage_presses or 999

        for position in self.buttons:
            joltage_difference = jolts_target[position] - current_state[position]
            max_press = min(joltage_difference, max_press)
            biggest_press = max(joltage_difference, biggest_press)

        min_press = biggest_press - finger_endurance
        min_press = min_press if min_press > 0 else 0

        return min_press, max_press + 1

    def press(self, n_presses: int = 1):
        return self.buttons if n_presses % 2 == 1 else [0]


class JoltageIndicator:
    n_indicators: int
    jolts_target: list[int]

    def __init__(self, joltage_instructions: str):
        self.jolts_target = [int(jolt) for jolt in joltage_instructions.split(",")]
        self.n_indicators = len(self.jolts_target)

    def __repr__(self):
        return f"Jolts target {self.jolts_target}"
    
    def __len__(self):
        return len(self.jolts_target)

    def charge(
        self, current_charge: list[int], positions: list[int], joltage_applied: int
    ):
        new_charge = current_charge.copy()
        for indicator in positions:
            new_charge[indicator] += joltage_applied

        return new_charge

    def maximum_joltage(self):
        return max(self.jolts_target)


class Machine:
    lights: Light
    buttons: list[Button]
    joltage: JoltageIndicator
    job: list[
        Button
    ]  # Joltage-Optimized Buttons are sorted according to the maximum number of times they can be pressed
    codex: list[System]
    free_variables: list[int]
    n_solutions: int = 0
    n_min_presses: int = 0

    def __init__(self, instructions: str):
        self.lights = Light(re.search(r"\[([^\]]+)\]", instructions).group(1))  # ty:ignore[possibly-missing-attribute]
        self.joltage = JoltageIndicator(
            re.search(r"\{([^}]+)\}", instructions).group(1)  # ty:ignore[possibly-missing-attribute]
        )

        self.console = Console()
        self.buttons = []
        for match in re.findall(r"\(([^)]+)\)", instructions):
            self.buttons.append(Button(match))

    def __repr__(self):
        return f"Machine with {self.n_lights} lights ({self.lights}), {self.n_buttons} buttons and a Joltage of {self.joltage}"

    @property
    def n_lights(self):
        return self.lights.n

    @property
    def n_buttons(self):
        return len(self.buttons)

    @property
    def is_started(self):
        return self.lights.is_lit

    @property
    def lights_state(self):
        return self.lights.state

    def test_buttons(self, buttons_sequence: list) -> bool:
        self.lights.reset()
        for button_position in buttons_sequence:
            self.lights.switch_lights(self.buttons[button_position].press())

        return self.lights.is_lit

    async def apply_science(self):
        codex = []
        self.debug_systems = []
        # Each joltage level equates to one system of equation for a given joltage counter
        for i in range(0, self.n_lights):
            # Each system will track if the button triggers the joltage counter or not
            system = [1 if button.targets(i) else 0 for button in self.buttons]
            # And the number of times the joltage counter needs to be triggered
            system.append(self.joltage.jolts_target[i])

            self.debug_systems.append(system.copy())
            codex.append(System(system))

        self.codex = codex

    async def reduce_systems(self):
        "Recursively shapes the matrix toward a row echelon"
        # Register the max number of presses for each button
        for i, button in enumerate(self.buttons):
            for system in self.codex:
                if system[i] != 0:
                    button.set_max_presses(system.joltage)
                if system.joltage > self.n_min_presses:
                    self.n_min_presses = system.joltage

        for row in range(0, len(self.codex)):
            system = self.codex[row]
            # Reduce the biggest system and order systems with biggest on top
            for inner_row in range(row + 1, len(self.codex)):
                system, new_system = await self._reduce(self.codex[inner_row], system)
                self.codex[row] = system
                self.codex[inner_row] = new_system

        return self.codex

    async def _reduce(
        self,
        system_a: System,
        system_b: System,
    ) -> tuple[System, System]:
        if system_b.non_leading_zero is None:
            return system_a, system_b
        if system_a.non_leading_zero is None:
            return system_b, system_a

        # No reduction is needed, simply return the ordered systems
        if system_a.non_leading_zero != system_b.non_leading_zero:
            if system_a.non_leading_zero < system_b.non_leading_zero:
                return system_a, system_b
            return system_b, system_a
        
        small_system = system_b
        big_system = system_a
        # Find the system to keep at the top and the one to reduce
        for col in range(0, len(system_a) - 1):
            if system_a[col] == system_b[col]:
                continue
            if (
                abs(system_a[col]) < abs(system_b[col]) or system_b[col] == 0
            ) and system_a[col] != 0:
                break

            small_system = system_a
            big_system = system_b
            break

        small_system.reduce(big_system)
        return big_system, small_system
        # if system_b.non_leading_zero is None:
        #     return system_a, system_b
        # if system_a.non_leading_zero is None:
        #     return system_b, system_a
            

        # system_b.reduce(system_a)
        # return system_a, system_b

    async def back_substitute(self):
        for i, reference in enumerate(self.codex):
            # Empty systems
            if reference.non_leading_zero is None:
                continue

            # Adds this variable to the list of non free variables
            self.buttons[reference.non_leading_zero].is_free_variable = False

            # Swith to a positive value in front
            if reference[reference.non_leading_zero] < 0:
                reference *= -1

            # Reduce other systems using this one
            for system in self.codex[:i]:
                if system[reference.non_leading_zero] == 0:
                    continue
                system.reduce(reference)

        for system in self.codex:
            if system.non_leading_zero is None:
                continue
            button = self.buttons[system.non_leading_zero]
            # Check if this system has a solution and register dependant variables
            button.solution = system.find_solution()
            if button.has_solution:
                self.n_solutions += 1

        self.free_variables = [
            i for i, button in enumerate(self.buttons) if button.is_free_variable
        ]

    async def solve(self):
        await self.frame_free_variables()
        if len(self.free_variables) == 0:
            return round(sum([button.solution for button in self.buttons]))

        max_joltage = self.joltage.maximum_joltage()
        answer = None

        for presses in self.enumerate_free_variables_presses():
            variables_presses = {
                var: presses[i] for i, var in enumerate(self.free_variables)
            }

            n_presses = sum(presses)
            for system in self.codex:
                buttons_pressed = system.count_presses(variables_presses) 

                # Remove invalid scenarii
                if buttons_pressed is None or not is_almost_integral(buttons_pressed, tolerance=0.01):
                    n_presses = None
                    break

                n_presses += round(buttons_pressed)
                    
                
            if n_presses is None:
                continue
            if n_presses < 0 or n_presses < max_joltage:
                self.console.print(f"Found invalid number of presses {n_presses} with {presses} ({max_joltage})")
                continue
            
            if n_presses == max_joltage:
                return n_presses
            if answer is None:
                answer = n_presses
                    
            if n_presses < answer:
                answer = n_presses
                    

        if answer != max_joltage:
            self.console.print(self.debug_systems)
            self.console.print(self.codex)
            self.console.print(f"{answer} vs {max_joltage}")
        return answer

    async def frame_free_variables(self):
        # Try to frame the min and max values of each free variables
        for variable in self.free_variables:
            # Find if this variable is in one of the above systems
            for i in range(0, min(variable, len(self.codex))):
                system = self.codex[i]
                if system.non_leading_zero is None:
                    continue
                if system.non_leading_zero >= variable:
                    break

                # Find if there is a codependant free variable
                has_codependance = False
                for j in range(system.non_leading_zero + 1, len(system) - 1):
                    if j == variable:
                        continue
                    if system[j] != 0:
                        has_codependance = True
                        break
                if has_codependance:
                    continue

                # Else frame min/max presses
                value = system[variable]
                if value == 0:
                    continue

                button = self.buttons[variable]
                presses = system.joltage / value

                if value > 0 and system.joltage > 0:
                    presses = floor(presses)
                    if system[system.non_leading_zero] > 0:
                        button.set_max_presses(presses)
                    else:
                        button.set_min_presses(presses)
                if value < 0 and system.joltage < 0:
                    presses= ceil(presses)
                    if system[system.non_leading_zero] > 0:
                        button.set_min_presses(presses)
                    else:
                        button.set_max_presses(presses)

    def enumerate_free_variables_presses(self) -> Iterable:
        return product(
            *[self.buttons[variable].range for variable in self.free_variables]
        )


class AOC2025Day10(AOCPuzzle):
    pass
