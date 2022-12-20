

__author__ = "Maximilian Geitner"
__date__ = "17.12.2022"

class Rock:

    def __init__(self, rock_str):
        self.w = 0

        parts = rock_str.split("\n")
        self.h = len(parts)
        self.w = len(parts[0])
        self.default_x = 2  # start position when dropping rock
        self.structure = []

        for part in parts:
            rock_row = []
            for letter in part:
                if letter == '#':
                    rock_row.append(True)
                else:
                    rock_row.append(False)
            self.structure.append(rock_row)

