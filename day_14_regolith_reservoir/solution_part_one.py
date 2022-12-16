
__author__ = "Maximilian Geitner"
__date__ = "14.12.2022"

from day_14_regolith_reservoir.helper_functions import get_next_pos, get_grid_boundaries, fill_grid

# Warning: Differences in the coordinate-format
# coordinate format = (y_pos, x_pos) within the grid structure
# coordinate format = (x_pos, y_pos) in the input

if __name__ == '__main__':
    FILENAME = 'input.txt'

    grid = []
    start_pos = (0, 500)
    # Step 1: file read iteration one: find minimum and maximum pos for coordinate system
    min_x, max_x, min_y, max_y = get_grid_boundaries(FILENAME)

    # Step 2: Create grid data structure
    amount_rows = max_y - min_y + 1
    amount_cols = max_x - min_x + 1
    # print(amount_rows, amount_cols)
    offset = (min_y, min_x)  # rock structure at (0, 0) in grid
    for i in range(amount_rows):
        val_row = []
        for j in range(amount_cols):
            val_row.append(0)
        grid.append(val_row)
    # Step 3: second file read iteration: mark rock structures in grid
    grid = fill_grid(FILENAME, grid, offset)

    # Step 4: let sand fall until one sand block falls into endless void
    counter = 0
    while True:
        result = get_next_pos(grid, offset, start_pos)
        if result is not None:
            counter += 1
            grid[result[0] - offset[0]][result[1] - offset[1]] = 2
        else:
            break

    print("Amounts of sand placed before falling into the void (Solution Part One): ", counter)
