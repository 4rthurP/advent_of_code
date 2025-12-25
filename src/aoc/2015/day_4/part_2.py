import re
from hashlib import md5

from .commons import AOC2015Day4


class AOC2015Day4Part1(AOC2015Day4):
    answer = 9962624
    example_answer = None

    def solve(self):
        n = 0
        while True:
            hash = md5(f"{self.input.strip()}{n}".encode()).hexdigest()
            if re.match("000000", hash):
                self.log(f"One AdventCoin has been succesfully mined using {n}: {hash}")
                break

            if n % 100000 == 0:
                self.log(f"Processing ... {n}/?")
            n += 1
        return n
