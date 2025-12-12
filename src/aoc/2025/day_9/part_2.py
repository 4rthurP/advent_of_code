from .commons import AOC2025Day9, RedTile, TilesRow, order_axis


class AOC2025Day9Part2(AOC2025Day9):
    verbose_output = True
    answer = 1652344888
    # skip_puzzle = True
    example_answer = 24
    tiles: list[RedTile]
    rows: dict[int, TilesRow]

    def solve(self):
        # Find map edges
        self.tiles = []
        self.rows = {}
        previous_tile = None
        for position in self.read_input():
            new_tile = RedTile(position)
            self.tiles.append(new_tile)

            if previous_tile is None:
                previous_tile = new_tile
                continue

            self.connect_red_tiles(previous_tile, new_tile)    
            previous_tile = new_tile

        # Loop back to the first tile to connect everything together
        self.connect_red_tiles(new_tile, self.tiles[0])

        # Find valid ranges inside the map edges
        first_row = min(self.rows.keys())
        last_row = max(self.rows.keys())
        for y in self.rows:
            current_row = self.rows[y]

            # First and last rows already only contains valid ranges, we need to adapt the mapping
            if y in (first_row, last_row):
                current_row.is_end_row = True
                
            current_row.map_valid_spaces()
        
        # for row in self.rows.values():
        #     self.log(row)

        # Find the biggest valid rectangle
        max_area = 0
        best_tiles = ()

        for i in range(0, len(self.tiles)):
            tile_a = self.tiles[i]
            for j in range(i, len(self.tiles)):
                tile_b = self.tiles[j]
                area = tile_a.area_between(tile_b)

                if area <= max_area:
                    continue

                # self.log(f"Checking {tile_a} - {tile_b} with size of {area}")
                if not self.square_in_valid_space(tile_a, tile_b):
                    continue

                self.log(f"New current best {area}: {tile_a} - {tile_b}")
                best_tiles = (tile_a, tile_b)
                max_area = area

        self.log(f"Found best pair of tiles {best_tiles} for a max area of {max_area}")
        return max_area    
    
    def connect_red_tiles(self, previous_tile: RedTile, new_tile: RedTile):
        direction = new_tile.find_direction(previous_tile)
        # self.log(f"New direction {direction} from {previous_tile} to {new_tile}")

        if direction == "horizontal":
            self.add_range(new_tile.y, previous_tile.x, new_tile.x)
            return
        
        if direction == "up":
            min_axis = previous_tile.y + 1
            max_axis = new_tile.y
        else:
            min_axis = new_tile.y
            max_axis = previous_tile.y
        
        for row in range(min_axis, max_axis):
            self.add_range(row, new_tile.x, new_tile.x)

    def add_range(self, y_pos: int, x_start: int, x_end: int):
        if y_pos not in self.rows:
            self.rows[y_pos] = TilesRow(y_pos)

        self.rows[y_pos].add_range(x_start, x_end)

            
    def square_in_valid_space(self, tile_a: RedTile, tile_b: RedTile):
        min_y, max_y = order_axis(tile_a.y, tile_b.y)
        # self.log(f"Validating rows {min_y} to {max_y}")
        for row in range(min_y, max_y):
            tiles_row = self.rows[row]
            # self.log(f"Checking: {tiles_row}")
            # If one row does not contain the rectangle we do not need to go further
            if not tiles_row.in_range(tile_a, tile_b):
                return False
        return True