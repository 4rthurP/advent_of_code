import polars as pl

from aoc.core.puzzle import AOCPuzzle


class AOC2025Day5Part2(AOCPuzzle):
    verbose_output = True
    answer = 348820208020395

    def solve(self):
        return self.polars()
    
    def polars(self):
        id_ranges = []

        for line in self.read_input():
            # Stop when reaching the second part of the file
            clean_line = line.strip()
            if clean_line == "":
                break

            id_range = clean_line.split("-", 1)
            id_ranges.append(
                {
                    "start": int(id_range[0]),
                    "end": int(id_range[1]),
                }
            )

        valid_ids = pl.DataFrame(
            id_ranges,
            schema={
                "start": pl.Int64,
                "end": pl.Int64,
            },
        ).sort(["start", "end"], descending=[False, True])

        counter = 0
        while True:
            old_size = valid_ids.height
            valid_ids = self.polars_cut_overlapping_ranges(valid_ids)
            # self.log(valid_ids)
            counter += 1
            if valid_ids.height == old_size:
                break
            # Remove overlaps until we cannot find any more of them

        self.log(f"Done in {counter} loops")

        ranges_sizes = valid_ids.with_columns(
            (pl.col("end") - pl.col("start") + 1).alias("n_valid_ids")
        )
        self.log(ranges_sizes)

        return ranges_sizes.sum()[0, "n_valid_ids"]

    def polars_cut_overlapping_ranges(self, ranges: pl.DataFrame) -> pl.DataFrame:
        valid_ids = ranges.clone()
        return (
            valid_ids.with_columns(
                (pl.col("start") - pl.col("end").shift(1, fill_value=1)).alias(
                    "start_overlap"
                ),
                (pl.col("end") - pl.col("end").shift(1, fill_value=1)).alias(
                    "end_overlap"
                ),
            )
            .filter(
                # Remove all ranges that are included in the previous range
                ~(pl.col("end_overlap") <= 0)
            )
            .with_columns(
                # Remove overlapping parts
                pl.when(pl.col("start_overlap") <= 0)
                .then(
                    # + 1 avoid repeating the end of the first period as the starting number of the second one
                    pl.col("start") - pl.col("start_overlap") + 1
                )
                .otherwise(pl.col("start"))
                .alias("new_start")
            )
            .select(
                pl.col("new_start").alias("start"),
                pl.col("end"),
            )
        )

    def nested_loops(self):
        return 1

    def successive_loops(self):
        return 1
