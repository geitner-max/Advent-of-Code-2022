
__author__ = "Maximilian Geitner"
__date__ = "14.12.2022"

from day_14_regolith_reservoir.helper_functions import get_next_pos, get_grid_boundaries, fill_grid

# Warning: Differences in the coordinate-format
# coordinate format = (y_pos, x_pos) within the grid structure
# coordinate format = (x_pos, y_pos) in the input

# Differences compared to Part One:
# --> Add two additional rows to the bottom of the grid:
#     One empty row and another filled row with rocks in order to simulate the scenario
# --> Add a few hundred columns on the left and right side of the grid
#     This space is necessary for simulating the complete sand filling outcome

if __name__ == '__main__':
    FILENAME = 'input.txt'

    grid = []
    start_pos = (0, 500)
    offset = (0, 0,)
    # Step 1: file read iteration one: find minimum and maximum pos for coordinate system
    min_x, max_x, min_y, max_y = get_grid_boundaries(FILENAME)

    # Step 2: Difference to part one is applied here, add additional rows and columns to grid
    amount_rows = max_y - min_y + 1 + 2  # add one additional row for "infinity" horizontal row
    amount_cols = max_x - min_x + 1 + 500  # add enough space in x-direction to expand hourglass
    min_x -= 250
    # Step 3: Create grid data structure
    offset = (min_y, min_x)  # rock structure at (0, 0) in grid
    for i in range(amount_rows):
        val_row = []
        for j in range(amount_cols):
            if i == amount_rows - 2:
                val_row.append(0)  # second last row is empty
            elif i == amount_rows - 1:
                val_row.append(1)  # set last row to rocks
            else:
                val_row.append(0)
        grid.append(val_row)

    # Step 4: second file read iteration: mark rock structures in grid
    grid = fill_grid(FILENAME, grid, offset)

    # Step 4: let sand fall until the next position is placed on the position x=500, y=0

    counter = 0
    while True:
        result = get_next_pos(grid, offset, start_pos)
        if result is not None and not (result[0] == 0 and result[1] == 500):
            # continue placing sand block onto map
            counter += 1
            grid[result[0] - offset[0]][result[1] - offset[1]] = 2
        else:
            # reached sand block, exit loop
            break
    # solution: all placed blocks + block to fill the position x=500, y=0
    print("Amount of sand blocks placed (Solution Part Two): ", counter + 1)
