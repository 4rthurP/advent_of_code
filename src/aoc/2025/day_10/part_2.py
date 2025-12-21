from pathlib import Path
import re
import asyncio

from .commons import AOC2025Day10, Machine
import functools as ft
import itertools as it
from typing import TYPE_CHECKING, Callable, Iterable, TypeVar

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparisonT

type Lights = list[bool]
type Button = set[int]
type Joltage = tuple[int, ...]
# type Machine = tuple[Lights, list[Button], Joltage]
T = TypeVar('T')


def joltage_cost(buttons: list[Button], joltage: Joltage):
    def groupby(itr: Iterable[T], key: Callable[[T], 'SupportsRichComparisonT']):
        return {k: list(v) for k, v in it.groupby(sorted(itr, key=key), key=key)}

    def sub_halve(j_a: Joltage, j_b: Joltage) -> Joltage:
        return tuple((a - b) // 2 for a, b, in zip(j_a, j_b))

    def press(btns: tuple[Button, ...]) -> Joltage:
        return tuple(sum(i in b for b in btns) for i in range(len(joltage)))

    def pattern(jolts: Joltage) -> Joltage:
        return tuple(n % 2 for n in jolts)

    all_btn_combos = (combo for n in range(len(buttons) + 1) for combo in it.combinations(buttons, n))
    press_patterns = groupby(all_btn_combos, lambda btns: pattern(press(btns)))

    @ft.cache
    def cost(jolts: Joltage) -> int:
        if not any(jolts):
            return 0
        elif any(j < 0 for j in jolts) or pattern(jolts) not in press_patterns:
            return sum(joltage)
        else:
            btn_combos = press_patterns[pattern(jolts)]
            return min(len(btns) + 2 * cost(sub_halve(jolts, press(btns))) for btns in btn_combos)

    return cost(joltage)


class AOC2025Day10Part2(AOC2025Day10):
    verbose_output = True
    answer = 17970
    example_answer = 33 
    # skip_puzzle = True

    def solve(self):
        # answer = []
        # test_path = Path("test_part_2.txt")
        # answer_path = Path("answer_part_2.txt")

        # test_array = test_path.read_text().splitlines()
        # answer_array = answer_path.read_text().splitlines()

        # for line in range(len(test_array)):
        #     exepected = int(answer_array[line])
        #     given = int(test_array[line])
        #     if exepected != given:
        #         self.log(f"Line {line + 1} does not match: expected {exepected}, got {given}")
        # # total = 0
        # # pushes = 0
        # # for machine_instructions in self.read_input():
        # #     n = asyncio.run(
        # #         self.charge_machine(machine_instructions)
        # #     ) 
        # #     pushes += n
        # #     answer.append(n)
        # #     # self.log(f"Final answer: {n}")

        # # # return pushes

        # # if self.solving_puzzle:
        # #     answer_file = Path("test_part_2.txt")
        # #     answer_file.write_text("\n".join(str(a) for a in answer))

        # return 0
        return asyncio.run(self.helping_the_elfes())
    
    async def helping_the_elfes(self) -> int:
        # pushes = await asyncio.gather(
        #     *[
        #         self.charge_machine(machine_instructions)
        #         for machine_instructions in self.read_input()
        #     ]
        # )

        # return sum(pushes)
        pushes = 0
        for machine_instructions in self.read_input():
            n = await self.charge_machine(machine_instructions)
            pushes += n
            # self.log(f"Final answer: {n}")

        return pushes

    async def charge_machine(self, instructions: str) -> int:
        machine = Machine(instructions)

        await machine.apply_science()
        await machine.reduce_systems()
        await machine.back_substitute()

        return await machine.solve()
