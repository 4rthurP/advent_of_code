from aoc.core.puzzle import AOCPuzzle


class AOC2025Day2Part1(AOCPuzzle):
    answer = 36862281418

    def solve(self):
        input = self.input
        invalid_ids: list[int] = []

        for segment in input.split(","):
            id_range = segment.split("-")
            start = int(id_range[0])
            end = int(id_range[1])
            
            start_size, end_size = self.get_size(start, end)
            # Process all sizes in the range, for example 777 - 5776 would need to find incorrect ids of sizes 3 and 4
            size_range = range(start_size, end_size + 1)
            for size in size_range:
                invalid_ids.extend(self.get_invalid_in_range(size, start, end))

        self.log(f"Found {len(invalid_ids)} invalid ids in total")
        invalid_ids = list(set(invalid_ids))
        answer = sum(invalid_ids)
        self.log(f"{len(invalid_ids)} distinct invalid ids for a total of {answer}.")

        return answer

    def get_invalid_in_range(self, target_size: int, start: int, end: int) -> list[int]:
        ids = []
        for size in range(1, target_size // 2 + 1):
            if target_size % size != 0:
                continue

            multiple = target_size // size
            for id_part in range(
                self.get_start(size, start if size == target_size // 2 + 1 else None),
                self.get_end(size) + 1,
            ):
                new_id = int(str(id_part) * multiple)
                # No need to process any more number for this size if we are over the end of the range
                if new_id > end:
                    break
                # Do not add ids outside the range and unecessary multiples
                if new_id >= start and new_id not in ids:
                    ids.append(new_id)

        return ids

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
