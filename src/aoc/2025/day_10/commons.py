from polars.selectors import enum
import re

from aoc.core.puzzle import AOCPuzzle

class System:
    system: list[float]
    non_leading_zero: int | None
    solution

    def __init__(self, system: list[float]):
        self.system = system

    def __repr__(self):
        return f"System {self.system}"
    
    def __getitem__(self, index: int):
        return self.system[index]
    
    def __iter__(self):
        return iter(self.system)
    
    def __len__(self):
        return len(self.system)
    
    def find_non_leading_zero(self):
        for col, n in enumerate(self.system):
            if n != 0:
                self.non_leading_zero = col
                return
            
        self.non_leading_zero = None
    
    def reduce(self, reference: System):
        if reference.non_leading_zero is None:
            return
        factor = self.system[reference.non_leading_zero] / reference[reference.non_leading_zero]
                
        for i in range(0, len(reference)):
            self[i] - factor * reference[i]

        self.find_non_leading_zero()
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
        return f"[{"".join(lights_schema)}]"
    
    def reset(self):
        self.current_state = [False for _ in range(self.n)]

    
    def switch_lights(self, buttons: list[int]):
        for press in buttons:
            self.current_state[press] = not self.current_state[press]
    

class Button:
    buttons: list[int]
    max_joltage_presses: int | None

    def __init__(self, button_instruction: str):
        self.buttons = [int(button) for button in button_instruction.split(",")]
        self.max_joltage_presses = None

    def __repr__(self):
        return f"Button targets {self.buttons}. !! Do not press more than {self.max_joltage_presses} times, machine breakage risk !!"

    def targets(self, position: int):
        return position in self.buttons

    def set_max_presses(self, n: int):
        "Keep the minimum value given to make sure a button is not pressed too many times."
        if not self.max_joltage_presses:
            self.max_joltage_presses = n
            return 
        if n >= self.max_joltage_presses:
            return
        self.max_joltage_presses = n

    def optimize_presses(self, jolts_target: list[int], current_state: list[int], finger_endurance: int) -> tuple[int, int]:
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
    
    def charge(self, current_charge: list[int], positions: list[int], joltage_applied: int):
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
    job: list[Button] # Joltage-Optimized Buttons are sorted according to the maximum number of times they can be pressed

    def __init__(self, instructions: str):
        self.lights = Light(re.search(r"\[([^\]]+)\]", instructions).group(1))
        self.joltage = JoltageIndicator(re.search(r"\{([^}]+)\}", instructions).group(1))
        self.buttons = []
        for match in re.findall(r"\(([^)]+)\)", instructions):
            self.buttons.append(Button(match))
            
        return
    
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
    
    def apply_science(self):
        codex = []
        # Each joltage level equates to one system of equation for a given joltage counter
        for i in range(0, self.n_lights):
            # Each system will track if the button triggers the joltage counter or not
            system = [1 if button.targets(i) else 0 for button in self.buttons]
            # And the number of times the joltage counter needs to be triggered
            system.append(self.joltage.jolts_target[i])

            codex.append(system)

        return codex

    
    def run_bj2o(self):
        "Buttons-Joltage Optimization Operation"

        self.job = []
        # Get the position of the sorted elements, from least required joltage to the most
        for position in sorted(range(len(self.joltage.jolts_target)), key=lambda i: self.joltage.jolts_target[i]):
            joltage = self.joltage.jolts_target[position]
            for button in self.buttons:
                if button.targets(position) and button not in self.job:
                    button.set_max_presses(joltage)
                    self.job.append(button)

        # Goes from button with the max allowed presses to the lest one
        self.job.reverse()

    # def charge(self) -> bool:
    #     "Charging may take time, please be patient."
        

    #     self.joltage.reset_charge()
    #     for button_position, times in buttons_sequence:
    #         self.joltage.charge(self.buttons[button_position].press(), times)
        
    #     return self.joltage.is_charged

class AOC2025Day10(AOCPuzzle):
    pass
