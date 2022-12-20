import numpy as np


__author__ = "Maximilian Geitner"
__date__ = "17.12.2022"

from day_17_pyroclastic_flow.helper_functions import is_in_list, move_to_side, move_downwards, append_row
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

    # Step 3: Stack 1000000000000 in two phases
    height_buffer = 0
    phase = 1
    # Phase 1: save jet stream pos, grid length (shows current tower height after trimming at full rows) and
    #          next rock pattern as a single entry
    #          If pattern duplicate is detected, loop has occured
    #          --> Increase height counter to the nearest value near the required rock placement limit
    #               by adding the height difference (between the two duplicate entries) and the amount of iterations
    # Phase 2: Run loop until the end
    occurred_entries = []
    ITERATIONS = 1000000000000
    idx = 0
    while idx < ITERATIONS:
        # bonus code block handling large index jump
        if phase == 1:
            total_height = len(grid) + height_buffer
            entry = [idx, jet_stream_pos, cur_rock_pattern_id, total_height, len(grid)]
            res_iter = is_in_list(occurred_entries, entry)
            if res_iter is not None:
                # found duplicate entry --> compute amount of iterations and height difference between both entries
                iter_first, jet_first, rock_first, height_first, height_buffer_first = occurred_entries[res_iter]
                height_diff = total_height - height_first
                iter_diff = idx - iter_first
                # --> switch to phase two
                phase = 2
                iter_left = ITERATIONS - 1 - idx  # amount of iterations left
                cycles = iter_left//iter_diff
                height_buffer = np.float64(height_buffer) + np.float64(cycles) * height_diff
                idx = idx + cycles * iter_diff
            else:
                occurred_entries.append(entry)

        # find current rock
        cur_rock = rocks[cur_rock_pattern_id]
        cur_rock_pattern_id = (cur_rock_pattern_id + 1) % len(rocks)

        # find position three blocks above current tower
        cur_x = cur_rock.default_x
        cur_y = len(grid) + 3 + (cur_rock.h - 1)  # len(grid) contains the amount of rows
        movement = 0
        # move rock until correct resting position is found
        while True:
            if movement == 0:
                # move sideways
                cur_x, jet_stream_pos = move_to_side(grid, cur_rock, cur_x, cur_y, jet_stream_pattern, jet_stream_pos)
            else:
                # move downwards and check whether rock can fall further
                ret_val = move_downwards(grid, cur_rock, cur_x, cur_y)
                if ret_val:
                    cur_y = cur_y - 1
                else:
                    # invalid position if moved downwards, place rock permanently on the grid
                    # fill grid up with empty rows
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
        # trim tower after one rotation of all rock types
        if cur_rock_pattern_id == 0:
            for j in range(max(len(grid) - 30, 0), len(grid)):
                full_row = True
                for i in range(7):
                    if not grid[j][i]:
                        full_row = False
                        break

                if full_row:
                    # shorten grid and exit this loop
                    height_buffer += j + 1
                    if j == len(grid) - 1:
                        grid = []
                    else:
                        grid = grid[j + 1:len(grid)]
                    break
        # loop counter increment
        idx = idx + 1

    print("Tower height after 1000000000000 Rocks (Solution Part Two): ", height_buffer + len(grid))
