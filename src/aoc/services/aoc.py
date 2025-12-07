import os
from pathlib import Path


def create_aoc_puzzle(day: int, year: int | None = None, parts: int = 2) -> tuple[bool, str]:
    year = year or int(os.environ.get("CURRENT_YEAR"))

    year_folder = Path(__file__).parent.parent / str(year) 
    input_file = year_folder / "inputs" / f"day_{day}.txt"
    example_input_file = year_folder / "inputs" / f"day_{day}_example.txt"
    puzzle_folder = year_folder / f"day_{day}"

    if not year_folder.exists():
        return False, "Year folder does not exist."

    template_file = year_folder / "puzzle_template.py"

    if not template_file.exists():
        return False, "Template file does not exist."

    puzzle_folder.mkdir(exist_ok=True)

    # Copy template for each part
    for part in range(1, parts + 1):
        part_file = puzzle_folder / f"part_{part}.py"
        if part_file.exists():
            continue # Easily create part one and re-run to create part two

        with template_file.open("r") as template:
            template_content = template.read()

        part_content = template_content.replace("DayX", f"Day{day}").replace("PartX", f"Part{part}")

        with part_file.open("w") as part:
            part.write(part_content)

    # Create empty input file
    if not input_file.exists():
        with input_file.open("w") as input:
            input.write("")

    # Create empty example input file
    if not example_input_file.exists():
        with example_input_file.open("w") as example_input:
            example_input.write("")

    return True, "AOC puzzle structure created successfully."

