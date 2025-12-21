import asyncio

from .commons import AOC2025Day10, Machine  # ty:ignore[unresolved-import]


class AOC2025Day10Part2(AOC2025Day10):
    # verbose_output = True
    answer = 17970
    example_answer = 33

    def solve(self):
        return asyncio.run(self.helping_the_elfes())

    async def helping_the_elfes(self) -> int:
        pushes = await asyncio.gather(
            *[
                self.charge_machine(machine_instructions)
                for machine_instructions in self.read_input()
            ]
        )

        return sum(pushes)

    async def charge_machine(self, instructions: str) -> int:
        machine = Machine(instructions)

        await machine.apply_science()
        await machine.bop_it()
        await machine.activate_drs()
        await machine.use_bts()
        await machine.holmes_protocole()
        await machine.mini_maxi_magigua()

        return await machine.solve()
