__author__ = "Maximilian Geitner"
__date__ = "08.12.2022"

# direction:
# 0: left
# 1: bottom
# 2: right
# 3: top


def is_visible(grid, amount_rows, r, c, direction):
    # helper function for part one
    # shows whether given tree is visible from a certain direction
    if direction == 0:
        # fixed row, column from 0 to (c -1) ==> direction left
        for i in range(c):
            if grid[r][i] >= grid[r][c]:
                return False
    elif direction == 1:
        # fixed column, from (r + 1) to end ==> direction bottom
        for j in range(r + 1, amount_rows):
            if grid[j][c] >= grid[r][c]:
                return False
    elif direction == 2:
        # fixed row, column from (c + 1) to end ==> direction right
        for i in range(c + 1, amount_rows):
            if grid[r][i] >= grid[r][c]:
                return False
    elif direction == 3:
        # fixed column, row from 0 to (r - 1) ==> direction top
        for j in range(r):
            if grid[j][c] >= grid[r][c]:
                return False
    return True


def get_blocked(grid, amount_rows, r, c, direction):
    # helper function for part two
    count = 1
    if direction == 0:
        # direction left
        for i in range(c - 1, 0, -1):
            if grid[r][i] >= grid[r][c]:
                return count
            elif i != 0:
                count += 1
    elif direction == 1:
        # direction bottom
        for j in range(r + 1, amount_rows):
            if grid[j][c] >= grid[r][c]:
                return count
            elif j != amount_rows - 1:
                count += 1
    elif direction == 2:
        # direction right
        for i in range(c + 1, amount_rows):
            if grid[r][i] >= grid[r][c]:
                return count
            elif i != amount_rows - 1:
                count += 1

    elif direction == 3:
        # direction top
        for j in range(r - 1, 0, -1):
            if grid[j][c] >= grid[r][c]:
                return count
            elif j != 0:
                count += 1
    return count


if __name__ == '__main__':

    file = open('input.txt', 'r')
    count_visible = 0
    grid_trees = []  # row, col

    amount_trees_row = 0
    # Initialize Grid
    for line in file:
        if amount_trees_row == 0:
            amount_trees_row = len(line) - 1 # amount of trees in one row

        entry = []
        for idx in range(amount_trees_row):
            entry.append(line[idx])
        grid_trees.append(entry)

    # Part One: Count trees that are visible
    for row in range(amount_trees_row):
        for col in range(amount_trees_row):
            if row == 0 or col == 0 or row == amount_trees_row - 1 or col == amount_trees_row -1:
                count_visible += 1  # trees at the edge are always visible
            else:
                # for interior trees: Count trees as visible if they are visible from at least one direction
                is_cell_visible = False
                for idx in range(4):
                    if is_visible(grid_trees, amount_trees_row, row, col, idx):
                        is_cell_visible = True
                        break
                if is_cell_visible:
                    count_visible += 1  # increase counter, if tree is visible from at least one direction

    print("Visible trees in the grid (Solution Part One): ", count_visible)
    # Part Two
    max_scenic = 1
    for row in range(amount_trees_row):
        for col in range(amount_trees_row):
            if row == 0 or col == 0 or row == amount_trees_row - 1 or col == amount_trees_row - 1:
                pass
            else:
                scenic_multiplier = 1
                for idx in range(4):
                    scenic_multiplier *= get_blocked(grid_trees, amount_trees_row, row, col, idx)
                if scenic_multiplier > max_scenic:
                    max_scenic = scenic_multiplier

    print("Highest scenic multiplier in the grid (Solution Part Two): ", max_scenic)
