import asyncio

from .commons import AOC2025Day10, Machine


class AOC2025Day10Part2(AOC2025Day10):
    verbose_output = True
    # answer = 0
    example_answer = 33
    # skip_puzzle = True

    def solve(self):
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
