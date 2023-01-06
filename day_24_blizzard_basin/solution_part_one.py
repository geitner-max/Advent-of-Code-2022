
__author__ = "Maximilian Geitner"
__date__ = "24.12.2022"

from day_24_blizzard_basin.helper_functions import build_grid, get_next, is_in_list
from day_24_blizzard_basin.storm import Storm


if __name__ == '__main__':
    file = open('input.txt', 'r')

    grid_walls = []
    storms = []
    EMPTY_TILE = 0
    WALL_TILE = 1  # Wall or storm in simulation
    EXIT_TILE = 2
    # Step 1: Read file
    cur_pos = None
    y = 0
    amount_cols = 0
    # Step 1: Read input
    for line in file:
        line = line.replace("\n", "")
        grid_row = []
        x = 0
        for letter in line:
            if letter == '#':
                grid_row.append(WALL_TILE)
            elif letter == '.':
                if cur_pos is None:
                    cur_pos = [y, x]
                grid_row.append(EMPTY_TILE)
            else:
                grid_row.append(EMPTY_TILE)
                # storm on this tile
                storms.append(Storm([y, x], letter))
            x += 1
        grid_walls.append(grid_row)
        y += 1
        amount_cols = x
    # Step 2: Compute amount of rows and start and destination position for given scenario
    amount_rows = y

    # Step two: Simulate region
    print("start", cur_pos)
    pos_list = [cur_pos]
    step = 0
    end_pos = None

    for x in range(amount_cols):
        if grid_walls[amount_rows - 1][x] == EMPTY_TILE:
            end_pos = [amount_rows - 1, x]
            break

    print("End: ", end_pos)

    # Step 3: For each iteration, perform one step in the simulation
    while True:
        next_possible_pos = []  # list contains positions that can be visited after this iteration
        # Step 3.1: Put current storm information into grid
        grid_storm = build_grid(grid_walls, amount_rows, amount_cols, storms)
        # Step 3.2: For each position in list, check neighbor pos and add to list if it can be visited
        for pos in pos_list:
            pos_next = get_next(pos, grid_storm, amount_rows, amount_cols)
            # print(pos_next)
            for candidate in pos_next:
                if not is_in_list(candidate, next_possible_pos):
                    next_possible_pos.append(candidate)
        # check if exit node is in list
        if is_in_list(end_pos, next_possible_pos):
            print("Number of Minutes to Avoid the Blizzards and Reach the Goal (Solution Part One): ", step)
            exit(0)
        else:
            # move storms one tile
            for storm in storms:
                storm.move_one_step(amount_rows, amount_cols, grid_walls)
        # prepare for next iteration
        step += 1
        pos_list = next_possible_pos

