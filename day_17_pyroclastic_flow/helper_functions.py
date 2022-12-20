
__author__ = "Maximilian Geitner"
__date__ = "17.12.2022"


def append_row(grid_inner):
    grid_inner.append([False] * 7)  # highest indexed row is the top of the tower
    pass


def is_valid_free_pos(grid_inner, x, y):
    amount_rows = len(grid_inner)
    if x < 0 or x >= 7:
        #print("Invalid x: ", x)
        return False  # block out of bounds
    else:
        # check if block might be in grid
        if 0 <= y < amount_rows:
            # if grid_inner[y][x]:
                # print("Invalid grid pos: ", x, y)
            # value True in grid = rock is placed there
            return not grid_inner[y][x]

    if y < 0:
        #print("Invalid y: ", y)
        return False
    else:
        return True


def move_to_side(grid, rock, x, y, pattern, pattern_pos):
    next_move = pattern[pattern_pos]
    next_pattern_pos = (pattern_pos + 1) % len(pattern)
    x_next = x + 1
    if next_move == '<':
        # move left
        x_next = x - 1
    # check new rock position
    for j in range(len(rock.structure)):
        row = rock.structure[j]
        for i in range(len(row)):
            # for each position in structure, check validity
            if row[i]:
                # rock position --> check if free in grid
                if not is_valid_free_pos(grid, x_next + i, y - j):
                    return x, next_pattern_pos
    # if valid position, then apply change
    return x_next, next_pattern_pos


def move_downwards(grid, rock, x, y):
    y_next = y - 1
    for j in range(len(rock.structure)):
        row = rock.structure[j]
        for i in range(len(row)):
            # for each position in structure, check validity
            if row[i]:
                if not is_valid_free_pos(grid, x + i, y_next - j):
                    return False
    # valid position for rock
    return True


def print_grid(g):
    output = ""
    for row in g:
        row_content = ""
        for val in row:
            if val == 0:
                row_content += "."
            elif val == 1:
                row_content += "#"
            else:
                row_content += "o"
        output = row_content + "\n" + output
    print(output)


def is_in_list(list_entries, entry_occurrence):
    for idx_list in range(len(list_entries)):
        iteration, jet_pos, rock_pattern, _, buffer = list_entries[idx_list]
        if jet_pos == entry_occurrence[1] and rock_pattern == entry_occurrence[2] and buffer == entry_occurrence[4]:
            return idx_list
    return None