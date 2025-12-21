import asyncio
from itertools import batched, permutations

from .commons import AOC2025Day10, Machine  # ty:ignore[unresolved-import]


class AOC2025Day10Part1(AOC2025Day10):
    answer = 477
    example_answer = 7

    def solve(self):
        return asyncio.run(self.helping_the_elfes())

    async def helping_the_elfes(self) -> int:
        n_pushes = 0
        for batch in batched(self.read_input(), 50, strict=False):
            pushes = await asyncio.gather(
                *[
                    self.start_machine(machine_instructions)
                    for machine_instructions in batch
                ]
            )
            n_pushes += sum(pushes)

        return n_pushes

    async def start_machine(self, machine_instructions: str) -> int:
        machine = Machine(machine_instructions)

        for n_pushes in range(1, machine.n_buttons):
            # Simply get the position of the buttons to push
            for permutation in permutations(range(machine.n_buttons), n_pushes):
                if machine.play_with_buttons(permutation):
                    self.log(
                        f"Machine {machine.lights_state} started in {n_pushes} presses: {permutation}"
                    )
                    return n_pushes

        self.log(f"Could not find the correct combination for {machine}")
        # Just need to press all buttons
        return machine.n_buttons
