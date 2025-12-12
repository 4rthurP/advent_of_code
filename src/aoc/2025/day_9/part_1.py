from .commons import AOC2025Day9, RedTile


class AOC2025Day9Part1(AOC2025Day9):
    verbose_output = True
    answer = 4764078684
    example_answer = 50

    def solve(self):
        # Find tiles and map valid positions of the floor
        self.tiles = [
            RedTile(position)
            for position in self.read_input()
        ]

        # Find the biggest valid rectangle
        max_area = 0
        best_tiles = ()

        for i in range(0, len(self.tiles)):
            tile_a = self.tiles[i]
            for j in range(i, len(self.tiles)):
                tile_b = self.tiles[j]
                area = tile_a.area_between(tile_b)

                if area > max_area:
                    best_tiles = (tile_a, tile_b)
                    max_area = area
        
        self.log(f"Best combination of tiles found with an area of {max_area}: {best_tiles}.")

        return max_area
    