
__author__ = "Maximilian Geitner"
__date__ = "17.12.2022"

from day_17_pyroclastic_flow.helper_functions import move_to_side, append_row, move_downwards
from day_17_pyroclastic_flow.rock import Rock


if __name__ == '__main__':
    FILENAME = 'input.txt'
    file = open(FILENAME, 'r')
    jet_stream_pattern = ""

    for line in file:
        jet_stream_pattern = line.replace("\n", "")
    file.close()

    rock_patterns = ["####", ".#.\n###\n.#.", "..#\n..#\n###", "#\n#\n#\n#", "##\n##"]
    rocks = []
    cur_rock_pattern_id = 0
    jet_stream_pos = 0
    # Step 1: Initialize Rocks from rock patterns
    for pattern in rock_patterns:
        rock = Rock(pattern)
        rocks.append(rock)

    # Step 2: Initialize base grid
    grid = []

    # Step 3: Add 2022 rocks step by step to grid
    for idx in range(2022):
        # find current rock
        cur_rock = rocks[cur_rock_pattern_id]
        cur_rock_pattern_id = (cur_rock_pattern_id + 1) % len(rocks)
        # find position three blocks above current tower
        cur_x = cur_rock.default_x
        cur_y = len(grid) + 3 + (cur_rock.h - 1)  # len(grid) contains the amount of rows
        movement = 0
        while True:
            if movement == 0:
                # move sideways
                cur_x, jet_stream_pos = move_to_side(grid, cur_rock, cur_x, cur_y, jet_stream_pattern, jet_stream_pos)
            else:
                ret_val = move_downwards(grid, cur_rock, cur_x, cur_y)
                if ret_val:
                    cur_y = cur_y - 1
                else:
                    # invalid position if moved downwards, place rock immediately
                    # fill grid up with elements
                    while len(grid) <= cur_y:
                        append_row(grid)
                    # place rock in grid
                    for j in range(len(cur_rock.structure)):
                        row = cur_rock.structure[j]
                        for i in range(len(row)):
                            if row[i]:
                                grid[cur_y - j][cur_x + i] = True
                    break
            movement = (movement + 1) % 2

    print("Tower height after 2022 Rocks (Solution Part One): ", len(grid))
