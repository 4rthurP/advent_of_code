# Commands
## Running the solution
Running the solution for a given day
```
aoc solve 11
```

## Creating a new day
Creating a new day from the template
```
aoc create 12
```

## Specifying a year
Using the -y argument:
```
aoc solve 11 -y 2025
```

Setting the default year to run:
```
aoc config year -v 2025
```

# Enabling the CLI
## Virtual-env setup (no install)
1. cd to the repo folder

2. Sync the packages
```
uv sync
```

3. Source the virtual-env file
```
source .venv/bin/activate
```

4. Run the command:
```
python src/aoc/main.py aoc 11 -y 2025
```

## Installing the CLI
```
uv tool install https://github.com/4rthurP/advent_of_code.git
```
