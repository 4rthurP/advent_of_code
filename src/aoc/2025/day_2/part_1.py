from aoc.core.puzzle import AOCPuzzle


class AOC2025Day2Part1(AOCPuzzle):
    answer: int = 19605500130

    def solve(self):
        input = self.input
        answer = 0

        for segment in input.split(","):
            id_range = segment.split("-")
            start = int(id_range[0])
            end = int(id_range[1])

            # Remove unecessary numbers with odd chars
            size, size_end = self.get_size(start, end)
            if size % 2 != 0:
                if size == size_end:
                    # Eliminate all impossible ranges like 100-150
                    continue
                start = self.get_start(size + 1)

            if size_end % 2 != 0:
                end = self.get_end(size_end - 1)

            ids = range(
                start,
                end + 1,
            )

            # Final size with new start and end
            size, size_end = self.get_size(start, end)
            if size != size_end:
                raise ValueError(
                    f"Start ({start}) and end ({end}) are not the same size."
                )

            for id_part in range(
                self.get_start(size // 2, start),
                self.get_end(size_end // 2) + 1,
            ):
                id = int(str(id_part) * 2)
                if id in ids:
                    answer += id

        return answer

    def get_start(self, size: int, start: int | None = None) -> int:
        num = "1"
        if start is not None:
            num = str(start)[0]
        return int(num + "0" * (size - 1))

    def get_end(self, size: int) -> int:
        return int("9" * (size))

    def get_size(self, start: int | str, end: int | str) -> tuple[int, int]:
        if isinstance(start, int):
            start = str(start)
        if isinstance(end, int):
            end = str(end)
        return len(start), len(end)

    def create_id(self, num: int) -> int:
        return int(str(num) * 2)
