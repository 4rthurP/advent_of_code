from aoc.core.puzzle import AOCPuzzle


def order_axis(tile_coordinate: int, opposite_coordinate: int) -> tuple[int, int]:
    return min(tile_coordinate, opposite_coordinate), max(tile_coordinate, opposite_coordinate)

class Tile:
    x: int
    y: int
    color: str
    def __init__(self, position: str):
        self.position = position

        coordinates = position.split(",")
        self.x = int(coordinates[0])
        self.y = int(coordinates[1])
    
    def __repr__(self):
        return f"{self.color} Tile at ({self.x}, {self.y})"

class RedTile(Tile):
    color = "Red"
    
    def area_between(self, opposite_tile: RedTile) -> int:
        min_x, max_x = order_axis(self.x, opposite_tile.x)
        min_y, max_y = order_axis(self.y, opposite_tile.y)

        return (max_x - min_x + 1) * (max_y - min_y + 1)
    
    def find_direction(self, previous_tile: RedTile):
        if self.y == previous_tile.y:
            return "horizontal"
        
        if self.y < previous_tile.y:
            return "down"
        
        return "up"
        
class TilesRange:
    y: int
    start: int
    end: int

    def __init__(self, y_pos: int, x_start: int, x_end: int):
        self.y = y_pos
        self.start = min(x_start, x_end)
        self.end = max(x_start, x_end)

    def __repr__(self):
        return f"{self.start}-{self.end}"

    @property
    def is_single_tile(self):
        return self.start == self.end
    
    def to_range(self, x_pos: int):
        if self.start == x_pos:
            raise ValueError("Cannot create a range at the same x position.")
        
        return TilesRange(self.y, self.start, x_pos)
    
    def contains(self, min_x: int, max_x: int):
        return self.start <= min_x and self.end >= max_x 

    def merge(self, next_range: TilesRange):
        return TilesRange(
            self.y,
            min(self.start, next_range.start),
            max(self.end, next_range.end),
        )       
    

class TilesRow:
    y: int
    ranges: dict[int, TilesRange]
    valid_ranges: dict[int, TilesRange]
    is_end_row: bool = False

    def __init__(self, y_pos: int):
        self.ranges = {}
        self.y = y_pos

    def __repr__(self):
        return f"Valid ranges in row {self.y}: {list(self.valid_ranges.values())}"

    def add_range(self, x_start: int, x_end: int):
        self._append_ranges(TilesRange(self.y, x_start, x_end))

    def _append_ranges(self, range: TilesRange):
        if range.start in self.ranges and range.is_single_tile:
            # Do not replace a range when simply connecting the end tile
            return
        self.ranges[range.start] = range

    def map_valid_spaces(self):
        self.valid_ranges = {}

        # For end rows we only need to take every ranges available
        if self.is_end_row:
            for range in self.ranges.values():
                if range.is_single_tile:
                    continue
                self.valid_ranges[range.start] = range
            return

        previous_range = None
        merge_ranges = False
        for range_start in sorted(self.ranges):
            new_range = self.ranges[range_start]
            if previous_range is None:
                previous_range = new_range
                merge_ranges = True
                continue
            
            # Single value added in some edge cases, we skip it and do not count it toward merging
            if new_range.is_single_tile and previous_range.end == new_range.start:
                continue
            
            # Merge every other range
            if merge_ranges:
                merged_range = previous_range.merge(new_range)
            self.valid_ranges[merged_range.start] = merged_range

            previous_range = new_range
            merge_ranges = not merge_ranges

        if merge_ranges and not previous_range.is_single_tile:
            # The row finished with this range and then goes in another direction
            return
        
        # Edge case were we have a succession of single_tile - range - single tile
        latest_range_index = max(self.valid_ranges.keys())
        latest_range = self.valid_ranges[latest_range_index]
        new_range = latest_range.merge(previous_range)
        self.valid_ranges.pop(latest_range_index)
        self.valid_ranges[new_range.start] = new_range
        

    def in_range(self, tile_a: RedTile, tile_b: RedTile) -> bool:
        min_x, max_x = order_axis(tile_a.x, tile_b.x)

        for range_start in sorted(self.valid_ranges.keys()):
            # We passed through every potential ranges or have overlapping ranges we can stop here
            if range_start >min_x:
                return False
            
            # We test the range
            if self.valid_ranges[range_start].contains(min_x, max_x):
                return True
        return False


class AOC2025Day9(AOCPuzzle):
    pass
