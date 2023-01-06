
__author__ = "Maximilian Geitner"
__date__ = "22.12.2022"


def is_sector_edge_change(grid_inner, next_pos, rows, cols):
    if next_pos[0] < 0 or next_pos[0] >= rows or next_pos[1] < 0 or next_pos[1] >= cols:
        # out of bounds of the grid
        # print("Out of bounds")
        return True
    elif grid_inner[next_pos[0]][next_pos[1]] == ' ':
        # print("Is empty", next_pos)
        return True
    else:
        return False


def get_sector_index(grid_inner, position, step_size_inner):
    idx_inner = 0
    for top_left in grid_inner:
        if top_left[0] <= position[0] < top_left[0] + step_size_inner \
                and top_left[1] <= position[1] < top_left[1] + step_size_inner:
            # within sector
            return idx_inner
        idx_inner += 1
    print("Error Position to Sector: ", position)
    return None


def dir_to_key(direction):
    if direction == 0:
        return 'R'
    elif direction == 1:
        return 'B'
    elif direction == 2:
        return 'L'
    elif direction == 3:
        return 'T'
    else:
        print("Error dir input")
        return None


def apply_offset_to_pos(next_anchor, offset, current_connection):
    # to return next_pos, direction
    step = current_connection['step']
    type_edge = current_connection['type']
    next_dir = current_connection['dir']
    next_pos = [next_anchor[0] + step * offset, next_anchor[1]]
    if type_edge == 'row':
        # change x-coordinate
        # print("Case Row")
        next_pos = [next_anchor[0], next_anchor[1] + step * offset]
    return next_pos, next_dir


# move one step
def get_next_pos(grid_inner, grid_s, pos, direction, edge_connections, step_size_inner, rows, cols):
    next_pos = pos.copy()
    direction_next = direction
    if direction == 0:
        # right
        next_pos[1] += 1
    elif direction == 2:
        next_pos[1] -= 1
    elif direction == 1:
        # bottom
        next_pos[0] += 1
    elif direction == 3:
        next_pos[0] -= 1
    else:
        print("Error direction, get_next_pos")
    # Step 1: calculate next position
    if is_sector_edge_change(grid_inner, next_pos, rows, cols):

        # Step 1.1: Find location within current sector
        current_sector = get_sector_index(grid_s, pos, step_size_inner) + 1
        # look at dict and calculate next position
        # Case 1: left, take top left as anchor
        # Case 2: top, row, take top left as anchor
        anchor_dir = 'TL'
        edge_type_outgoing = 'row'
        if direction == 0:
            # Case 3: right, column, take top right as anchor
            anchor_dir = 'TR'
            edge_type_outgoing = 'col'
        elif direction == 1:
            # Case 4: bottom, row, take bottom left as anchor
            anchor_dir = 'BL'
        elif direction == 2:
            edge_type_outgoing = 'col'
        anchor = get_anchor(grid_s, current_sector, anchor_dir, step_size_inner)
        if edge_type_outgoing == 'col':
            # check y-coordinate difference
            offset = pos[0] - anchor[0]
        else:
            # check x-coordiante difference
            offset = pos[1] - anchor[1]
        if offset < 0 or offset >= step_size_inner:
            print("Error Offset")
        # Step 1.2: Find location in next sector on destination edge and the new direction
        current_connection = edge_connections[current_sector - 1]
        key = dir_to_key(direction)
        relevant_connection = current_connection[key]
        # calculate new position
        next_anchor = get_anchor(grid_s, relevant_connection['sector'], relevant_connection['anchor'], step_size_inner)

        next_pos, direction_next = apply_offset_to_pos(next_anchor, offset, relevant_connection)
    # Step 2: Look if position contains wall
    # check wall
    if grid_inner[next_pos[0]][next_pos[1]] == '#':
        # tile contains wall --> stay at old position
        return pos, direction
    return next_pos, direction_next


def fill_up_grid(grid_inner, cols):
    for x_idx in range(len(grid_inner)):
        row = grid_inner[x_idx]
        if len(row) < cols:
            row += (" " * (cols - len(row)))
        grid_inner[x_idx] = row
    return grid_inner


def move_amount(grid_inner, grid_s, steps, pos, direction, dict_edges_inner, rows, cols):
    for x_idx in range(steps):
        # grid, grid_sectors, pos, direction, edge_connections,  step_size, amount_rows, amount_cols
        next_pos, direction = get_next_pos(grid_inner, grid_s, pos, direction, dict_edges_inner, step_size, rows, cols)
        if next_pos == pos:
            # didnt move --> immeditately return function
            # print(next_pos, direction)
            return next_pos, direction
        else:
            pos = next_pos
            if visited[pos[0]][pos[1]] == -3:
                print("Error: Visited wall", pos)
            elif pos[0] < 0 or pos[0] >= len(visited) or pos[1] < 0 or pos[1] >= len(visited[0]):
                print("Invalid Pos: ", pos)
            else:
                visited[pos[0]][pos[1]] = direction
            # print(next_pos, direction)

    return pos, direction


# y-coordinate first
def get_anchor(grid_inner, req_sector, anchor, step_size_inner):
    sector_index = req_sector - 1
    if anchor == 'TL':
        # top left
        return grid_inner[sector_index].copy()
    elif anchor == 'TR':
        return [grid_inner[sector_index][0], grid_inner[sector_index][1] + step_size_inner - 1]
    elif anchor == 'BL':
        return [grid_inner[sector_index][0] + step_size_inner - 1, grid_inner[sector_index][1]]
    elif anchor == 'BR':
        return [grid_inner[sector_index][0] + step_size_inner - 1, grid_inner[sector_index][1] + step_size_inner - 1]
    else:
        print("Error")
        return None


# return, anchor point and direction
def convert_to_anchor(target_edge, step):
    if target_edge == 'T':
        if step == 1:
            return 'TL', 1, 'row'
        else:
            return 'TR', 1, 'row'
    elif target_edge == 'B':
        if step == 1:
            return 'BL', 3, 'row'
        else:
            return 'BR', 3, 'row'
    elif target_edge == 'L':
        if step == 1:
            return 'TL', 0, 'col'
        else:
            return 'BL', 0, 'col'
    elif target_edge == 'R':
        if step == 1:
            return 'TR', 2, 'col'
        else:
            return 'BR', 2, 'col'


def convert_edges_information(list_before):
    result = []
    for item in list_before:
        dict_sector = {}
        for value in item:

            res_obj = {'step': value['step'], 'sector': value['sector']}
            anchor, direction, type_edge = convert_to_anchor(value['dest'], value['step'])
            res_obj['anchor'] = anchor
            res_obj['dir'] = direction
            res_obj['type'] = type_edge
            dict_sector[value['src']] = res_obj
        result.append(dict_sector)
    return result


def convert_edge_information(sector, dest_edge, step):
    res_obj = {'step': step, 'sector': sector}
    anchor, direction, type_edge = convert_to_anchor(dest_edge, step)
    res_obj['anchor'] = anchor
    res_obj['dir'] = direction
    res_obj['type'] = type_edge
    return res_obj


def create_edge_entry(dest_sec, dest_edge, step):
    # {'anchor': 'TR', 'step': 1, 'sector': 6, 'type': 'col', 'dir': 2}
    return convert_edge_information(dest_sec, dest_edge, step)


# Data transformation: For each edge (src_sec, src_edge, dest_sec, dest_edge, step):
#               Create connection src -> dest and dest -> src
#               Each entry consists of following information:
#                   Sector & edge points to entry: (dest_sec, anchor, step, dir, type)
def expand_edge_information(list_edges_inner):
    result = []  # 6 sectors
    for _ in range(6):
        result.append({})
    # print(result)
    for edge in list_edges_inner:
        src_idx = edge['src_sec'] - 1
        dest_idx = edge['dest_sec'] - 1
        # src to dest connection
        dest_edge = create_edge_entry(edge['dest_sec'], edge['dest_edge'], edge['step'])
        # dest to src connection
        src_edge = create_edge_entry(edge['src_sec'], edge['src_edge'], edge['step'])
        result[src_idx][edge['src_edge']] = dest_edge
        result[dest_idx][edge['dest_edge']] = src_edge
    # print(result)
    return result


def print_visited_grid(grid_visited):
    output = ""
    for y_idx in range(len(grid_visited)):
        for x_idx in range(len(grid_visited[y_idx])):
            val = grid_visited[y_idx][x_idx]
            if val == -1:
                # not used
                output += " "
            elif val == 0:
                output += ">"
            elif val == 1:
                output += "v"
            elif val == 2:
                output += "<"
            elif val == 2:
                output += "^"
            elif val == -2:
                output += "."
            elif val == -3:
                output += "#"
        output += "\n"
    print(output)


if __name__ == '__main__':
    # 10R5L5R10L3L6R1
    # 10R5L5R10L5R2L4L4L4R2L2R3R1
    COMPUTE_EXAMPLE = False  # Compute example solution

    visited = []
    state = 0
    facing_dir = 0  # 0: right, 1: down, etc.
    cur_pos = None
    instructions = ""
    grid = []
    amount_rows = 0
    amount_cols = None
    if not COMPUTE_EXAMPLE:
        print("Compute solution for puzzle input...")
        # ---------- WARNING: Hardcoded values for given scenario ----------
        # list_edges contains the information connecting edges on a cube, specified by the side of the sectors
        #               and a certain step value to compute the offset
        # step_size specifies the amount of tiles per sector edge
        # direction: 0=right, 1=bottom, 2=left, 3=top
        # R: 6R+, L: 3T+, T: 2T+
        # edge side contains information about type and dir
        # +/- contains information about anchor and step
        step_size = 50
        list_edges = [
            {'src_sec': 1, 'src_edge': 'T', 'dest_sec': 6, 'dest_edge': 'L', 'step': 1},
            {'src_sec': 1, 'src_edge': 'L', 'dest_sec': 4, 'dest_edge': 'L', 'step': -1},
            {'src_sec': 2, 'src_edge': 'T', 'dest_sec': 6, 'dest_edge': 'B', 'step': 1},
            {'src_sec': 2, 'src_edge': 'R', 'dest_sec': 5, 'dest_edge': 'R', 'step': -1},
            {'src_sec': 2, 'src_edge': 'B', 'dest_sec': 3, 'dest_edge': 'R', 'step': 1},
            {'src_sec': 3, 'src_edge': 'L', 'dest_sec': 4, 'dest_edge': 'T', 'step': 1},
            {'src_sec': 5, 'src_edge': 'B', 'dest_sec': 6, 'dest_edge': 'R', 'step': 1},
        ]
        filename = 'input.txt'
    # ---------- Hardcoded Parameters for given example ----------
    else:
        print("Compute solution for example...")
        step_size = 4
        filename = 'test.txt'
        list_edges = [
            {'src_sec': 1, 'src_edge': 'T', 'dest_sec': 2, 'dest_edge': 'T', 'step': 1},
            {'src_sec': 1, 'src_edge': 'R', 'dest_sec': 6, 'dest_edge': 'R', 'step': 1},
            {'src_sec': 1, 'src_edge': 'L', 'dest_sec': 3, 'dest_edge': 'T', 'step': 1},
            {'src_sec': 2, 'src_edge': 'L', 'dest_sec': 6, 'dest_edge': 'B', 'step': -1},
            {'src_sec': 2, 'src_edge': 'B', 'dest_sec': 5, 'dest_edge': 'B', 'step': -1},
            {'src_sec': 3, 'src_edge': 'B', 'dest_sec': 5, 'dest_edge': 'L', 'step': -1},
            {'src_sec': 4, 'src_edge': 'R', 'dest_sec': 6, 'dest_edge': 'T', 'step': -1},
        ]

    dict_edge_connections = expand_edge_information(list_edges)
    # Step 1: Read input
    file = open(filename, 'r')
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
                        cur_pos = [0, i]  # (y, x) - coordinate
                        break
                amount_cols = len(line)
            else:
                amount_cols = max(len(line), amount_cols)
    file.close()
    amount_rows = len(grid)
    grid = fill_up_grid(grid, amount_cols)
    # Step 2: Fill up grid with empty tiles
    for y in range(amount_rows):
        row_content = []
        for x in range(amount_cols):
            if grid[y][x] == ' ':
                row_content.append(-1)  # not filled
            elif grid[y][x] == '.':
                row_content.append(-2)  # empty
            elif grid[y][x] == '#':
                row_content.append(-3)
            else:
                # not used tile
                print("Error Fill: ", grid[y][x])
                row_content.append(0)
        visited.append(row_content)

    grid_sectors = []  # contains top left coordinate of sector
    # Step 3: Identify sector anchor position (top-left corner of sector)
    for y in range(0, amount_rows, step_size):
        for x in range(0, amount_cols, step_size):
            if grid[y][x] != ' ':
                # sector filled
                grid_sectors.append([y, x])

    idx = 0
    cur_input = ""
    # Step 4: Follow instructions step-by-step, special for part two: treating map as a cube
    while idx <= len(instructions):
        if idx == len(instructions) or instructions[idx] == 'L' or instructions[idx] == 'R':
            # process input
            amount = int(cur_input)
            # grid, grid_sectors, steps, pos, direction, dict_edge_connections, amount_rows, amount_cols
            cur_pos, facing_dir = move_amount(grid, grid_sectors, amount, cur_pos, facing_dir,
                                              dict_edge_connections, amount_rows, amount_cols)
            # print("Steps: ", amount, " in direction", facing_dir, "-->", cur_pos, )
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

    # Step 5: Calculate solution by using the current position and the facing direction
    print("Position: ", cur_pos, " Direction: ", facing_dir)
    cur_pos[0] += 1  # y: row
    cur_pos[1] += 1  # x: column
    final_password = 1000 * cur_pos[0] + 4 * cur_pos[1] + facing_dir

    print("Final Password (Solution Part Two): ", final_password)
    # print_visited_grid(visited)
