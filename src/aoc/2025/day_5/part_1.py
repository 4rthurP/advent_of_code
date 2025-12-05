from aoc.core.puzzle import AOCPuzzle


class AOC2025Day5Part1(AOCPuzzle):
    # verbose_output = True
    answer = 681

    def solve(self):
        is_id_range = True

        valid_ids: list[tuple[int, int]] = []
        fresh_items = []

        for line in self.read_input():
            clean_line = line.strip()
            if clean_line == "":
                is_id_range = False
                valid_ids = list(set(valid_ids))
                continue

            if is_id_range:
                id_range = clean_line.split("-", 1)
                valid_ids.append((int(id_range[0]), int(id_range[1])))
                continue
            
            item_id = int(clean_line)
            for valid_range in valid_ids:
                if item_id >= valid_range[0] and item_id <= valid_range[1]:
                    fresh_items.append(item_id)
                    self.log(f"Found fresh item {item_id} in range {valid_range}")
                    break

        self.log(f"Found {len(fresh_items)} fresh items")
        return len(fresh_items)