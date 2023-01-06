
__author__ = "Maximilian Geitner"
__date__ = "22.12.2022"


def get_next_pos(pos, direction, grid_inner):
    # print(direction)
    # check validity
    if direction % 2 == 0:
        # out of map bounds --> go to first pos in row
        ret = next_pos_in_row(grid_inner, pos, facing_dir)
        if ret is None:
            return pos  # next position is invalid, cannot move
        else:
            # valid index, move to position
            return [pos[0], ret]
    else:

        ret = next_pos_in_column(grid_inner, pos, facing_dir)
        if ret is None:
            return pos  # next position is invalid, cannot move
        else:
            # valid index, move to position
            return [ret, pos[1]]


def next_pos_in_column(grid_inner, pos, direction):
    col_index = pos[1]
    index = pos[0]
    amount_rows = len(grid_inner)
    if direction == 1:
        # move down
        index = (index + 1) % amount_rows
        while col_index >= len(grid_inner[index]) or grid_inner[index][col_index] == ' ':
            # move one position to the right
            index = (index + 1) % amount_rows
        # print(index, amount_rows, col_index, len(grid_inner[col_index]))
        if grid_inner[index][col_index] == '.':
            return index
        elif grid_inner[index][col_index] == '#':
            return None
        else:
            print("Error: Stopped on empty tile")
    elif direction == 3:
        # move up
        index = (index + amount_rows - 1) % amount_rows
        while col_index >= len(grid_inner[index]) or grid_inner[index][col_index] == ' ':
            # move one position to the right
            index = (index + amount_rows - 1) % amount_rows
        # print(index, amount_rows, col_index, len(grid_inner[col_index]))
        if grid_inner[index][col_index] == '.':
            return index
        elif grid_inner[index][col_index] == '#':
            return None
        else:
            print("Error: Stopped on empty tile")
    print("Error direction Col")
    return None


def next_pos_in_row(grid_inner, pos, direction):
    row_index = pos[0]
    index = pos[1]
    amount_cols = len(grid_inner[row_index])
    if direction == 0:
        # move right
        index = (index + 1) % amount_cols
        while grid_inner[row_index][index] == ' ':
            # move one position to the right
            index = (index + 1) % amount_cols

        if grid_inner[row_index][index] == '.':
            return index
        elif grid_inner[row_index][index] == '#':
            return None
        else:
            print("Error: Stopped on empty tile")
    elif direction == 2:
        # move left
        index = (index + amount_cols - 1) % amount_cols
        while grid_inner[row_index][index] == ' ':
            # move one position to the right
            index = (index + amount_cols - 1) % amount_cols
        if grid_inner[row_index][index] == '.':
            return index
        elif grid_inner[row_index][index] == '#':
            return None
        else:
            print("Error: Stopped on empty tile")
    print("Error direction Row: ", direction)
    return None


def fill_up_grid(grid_inner, amount_cols):
    for x in range(len(grid_inner)):
        row = grid_inner[x]
        if len(row) < amount_cols:
            # print("Fill up")
            row += (" " * (amount_cols - len(row)))
        # print(len(row), amount_cols)
        grid_inner[x] = row
    return grid_inner


# moved fixed amount of steps
def move_amount(steps, pos, direction, grid_inner):
    for x in range(steps):
        next_pos = get_next_pos(pos, direction, grid_inner)
        if next_pos == pos:
            # didnt move
            return next_pos
        else:
            pos = next_pos
    return pos


if __name__ == '__main__':
    file = open('input.txt', 'r')

    state = 0
    facing_dir = 0  # 0: right, 1: down, etc.
    cur_pos = None
    instructions = ""
    grid = []
    amount_rows = 0
    amount_cols = None

    # Step 1: Read input
    for line in file:
        line = line.replace("\n", "")
        if line == "":
            # empty line deteced
            state = 1
        elif state == 1:
            # last line instructions
            instructions = line
        else:
            # map input
            grid.append(line)
            if amount_cols is None:
                # first line, initialize initial position
                for i in range(len(line)):
                    if line[i] == ".":
                        # first valid tile
                        cur_pos = (0, i)  # (y, x) - coordinate
                        break
                amount_cols = len(line)
            else:
                amount_cols = max(len(line), amount_cols)
    amount_rows = len(grid)
    grid = fill_up_grid(grid, amount_cols)

    idx = 0
    cur_input = ""
    # Step 2: Follow instructions step by step
    # Movement --> Turn Left or Right --> Movement --> etc.
    while idx <= len(instructions):
        if idx == len(instructions) or instructions[idx] == 'L' or instructions[idx] == 'R':
            # process input
            amount = int(cur_input)
            cur_pos = move_amount(amount, cur_pos, facing_dir, grid)
            if idx < len(instructions):
                cur_input = ""  # reset amount
                # read turn direction instruction
                if instructions[idx] == 'L':
                    facing_dir = (facing_dir + 3) % 4
                elif instructions[idx] == 'R':
                    facing_dir = (facing_dir + 1) % 4
                else:
                    print("Error facing direction instruction")
        else:
            cur_input += instructions[idx]
        idx += 1

    file.close()
    # Step 3: Calculate solution by using the current position and the facing direction
    print("Position: ", cur_pos, " Direction: ", facing_dir)
    cur_pos[0] += 1  # y: row
    cur_pos[1] += 1  # x: column
    final_password = 1000 * cur_pos[0] + 4 * cur_pos[1] + facing_dir

    print("Final Password (Solution Part One): ", final_password)
