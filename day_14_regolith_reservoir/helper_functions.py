
__author__ = "Maximilian Geitner"
__date__ = "14.12.2022"


def print_grid(g):
    output = ""
    for row in g:
        for val in row:
            if val == 0:
                output += "."
            elif val == 1:
                output += "#"
            else:
                output += "o"
        output += "\n"
    print(output)


def is_valid_x(grid, offset, pos_x):
    return offset[1] <= pos_x < offset[1] + len(grid[0])


def get_next_pos(grid, offset, cur_pos,):
    y_next = cur_pos[0] + 1
    x_cur = cur_pos[1]
    if y_next < offset[0] or y_next >= offset[0] + len(grid):
        # print("Invalid down", y_next, offset[0], len(grid))
        return None  # Position lies outside of grid
    else:
        # valid pos y, calculate next pos x
        y_next_mod = y_next - offset[0]
        x_cur_mod = x_cur - offset[1]
        # Case 1: One step down
        if grid[y_next_mod][x_cur_mod] == 0:
            # free field, fall here
            return get_next_pos(grid, offset, (y_next, x_cur,))
        elif not is_valid_x(grid, offset, x_cur - 1):
            # sand moves to endless void position
            # print("Invalid down-left")
            return None
        elif grid[y_next_mod][x_cur_mod - 1] == 0:
            return get_next_pos(grid, offset, (y_next, x_cur - 1,))
        elif not is_valid_x(grid, offset, x_cur + 1):
            # sand moves to endless void position
            # print("Invalid down-right")
            return None
        elif grid[y_next_mod][x_cur_mod + 1] == 0:
            return get_next_pos(grid, offset, (y_next, x_cur + 1,))
        else:
            # all three next possible positions are blocked, stay at the same coordinate
            return cur_pos


def get_grid_boundaries(filename):
    min_x = 500
    max_x = 500
    min_y = 0
    max_y = 0
    file = open(filename, 'r')
    for line in file:
        # split into coordinates
        parts = line.replace("\n", "").split(" -> ")

        for part in parts:
            pos_converted = part.split(",")
            x_pos = int(pos_converted[0])
            y_pos = int(pos_converted[1])

            min_x = min(min_x, x_pos)
            max_x = max(max_x, x_pos)
            min_y = min(min_y, y_pos)
            max_y = max(max_y, y_pos)
    file.close()
    return min_x, max_x, min_y, max_y


def fill_grid(filename, grid, offset):
    file = open(filename, 'r')
    for line in file:
        # split into coordinates
        parts = line.replace("\n", "").split(" -> ")

        # for each successive pair of points in the line, draw a line onto the grid
        # line is either vertical or horizontal
        for i in range(len(parts) - 1):
            coord_0 = list(map(lambda x: int(x), parts[i].split(",")))
            # mark path from coordinate one to coordinate two as rock structure
            coord_1 = list(map(lambda x: int(x), parts[i + 1].split(",")))
            if coord_0[0] == coord_1[0]:
                min_y_local = min(coord_1[1], coord_0[1])
                max_y_local = max(coord_1[1], coord_0[1])
                # x-pos stays the same
                amount = max_y_local - min_y_local + 1
                for y_offset in range(amount):
                    x_new = coord_0[0] - offset[1]
                    y_new = min_y_local - offset[0] + y_offset
                    grid[y_new][x_new] = 1
            else:
                min_x_local = min(coord_1[0], coord_0[0])
                max_x_local = max(coord_1[0], coord_0[0])
                # y-pos stays the same
                amount = max_x_local - min_x_local + 1
                for x_offset in range(amount):
                    x_new = min_x_local - offset[1] + x_offset
                    y_new = coord_0[1] - offset[0]
                    # print(x_new, y_new)
                    grid[y_new][x_new] = 1
    file.close()
    return grid
