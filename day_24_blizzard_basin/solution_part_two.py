
__author__ = "Maximilian Geitner"
__date__ = "24.12.2022"

from day_24_blizzard_basin.helper_functions import build_grid, get_next, is_in_list
from day_24_blizzard_basin.storm import Storm

# modified code from part one that calculates the time required to move from start to destination position
def steps_from_a_to_b(start_pos, end, grid_walls, list_storms, rows, cols):
    pos_list = [start_pos]
    step = 0
    while True:
        next_possible_pos = []  # list contains positions that can be visited after this iteration
        # Step 3.1: Put current storm information into grid
        grid_storm = build_grid(grid_walls, amount_rows, amount_cols, list_storms)
        # Step 3.2: For each position in list, check neighbor pos and add to list if it can be visited
        for pos in pos_list:
            pos_next = get_next(pos, grid_storm, rows, cols)
            # print(pos_next)
            for candidate in pos_next:
                if not is_in_list(candidate, next_possible_pos):
                    next_possible_pos.append(candidate)
        # check if exit node is in list
        if is_in_list(end, next_possible_pos):
            print("Exit reached after ", step, " minutes")
            return step, list_storms
        else:
            # move storms one tile
            for storm in list_storms:
                storm.move_one_step(amount_rows, amount_cols, grid_walls)
        step += 1
        pos_list = next_possible_pos


if __name__ == '__main__':
    file = open('input.txt', 'r')

    grid_walls = []
    storms = []
    EMPTY_TILE = 0
    WALL_TILE = 1  # Wall or storm in simulation
    EXIT_TILE = 2
    # Step 1: Read file
    initial_pos = None
    y = 0
    amount_cols = 0

    for line in file:
        line = line.replace("\n", "")
        grid_row = []
        x = 0
        for letter in line:
            if letter == '#':
                grid_row.append(WALL_TILE)
            elif letter == '.':
                if initial_pos is None:
                    initial_pos = [y, x]
                grid_row.append(EMPTY_TILE)
            else:
                grid_row.append(EMPTY_TILE)
                # storm on this tile
                storms.append(Storm([y, x], letter))
            x += 1
        grid_walls.append(grid_row)
        y += 1
        amount_cols = x
    # Step 2: Configure variables
    amount_rows = y

    # Step two: Simulate region
    print("start", initial_pos)

    total_steps = 0
    end_pos = None

    for x in range(amount_cols):
        if grid_walls[amount_rows - 1][x] == EMPTY_TILE:
            end_pos = [amount_rows - 1, x]
            break

    print("End: ", end_pos)

    # Step 3: Perform one step in the simulation
    step1, storms = steps_from_a_to_b(initial_pos, end_pos, grid_walls, storms, amount_rows, amount_cols)
    # Step 4: Go from end to start
    step2, storms = steps_from_a_to_b(end_pos, initial_pos, grid_walls, storms, amount_rows, amount_cols)
    step3, storms = steps_from_a_to_b(initial_pos, end_pos, grid_walls, storms, amount_rows, amount_cols)

    total_time = step1 + step2 + step3
    print("Total Amount of Minutes for Route Start --> End --> Start --> End (Solution Part Two): ", total_time)
