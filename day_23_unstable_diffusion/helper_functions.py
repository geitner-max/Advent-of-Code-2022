
__author__ = "Maximilian Geitner"
__date__ = "23.12.2022"


def is_in_list(pos, list_pos):
    for p in list_pos:
        if pos[0] == p[0] and pos[1] == p[1]:
            return True
    return False


def find_min_pos(list_pos):
    min_pos = list_pos[0].copy()
    for pos in list_pos:
        min_pos[0] = min(min_pos[0], pos[0])
        min_pos[1] = min(min_pos[1], pos[1])
    return min_pos


def find_max_pos(list_pos):
    min_pos = list_pos[0].copy()
    for pos in list_pos:
        min_pos[0] = max(min_pos[0], pos[0])
        min_pos[1] = max(min_pos[1], pos[1])
    return min_pos


def print_map(list_elfs):
    min_pos = find_min_pos(list_elfs)
    max_pos = find_max_pos(list_elfs)
    content = ""

    for y in range(min_pos[0], max_pos[0] + 1):
        row_content = ""
        for x in range(min_pos[1], max_pos[1] + 1):
            if is_in_list([y, x], list_elfs):
                row_content += "#"
            else:
                row_content += "."
        row_content += "\n"
        content += row_content
    print(content)


def set_val(grid_inner, pos, offset_inner, value):
    y_inner = pos[0] + offset_inner[0]
    x = pos[1] + offset_inner[1]
    grid_inner[y_inner][x] = value


def get_val(grid_inner, pos, offset_inner):
    y_inner = pos[0] + offset_inner[0]
    x = pos[1] + offset_inner[1]
    # print(y_inner, x, offset_inner, len(grid_inner), len(grid_inner[0]))
    return grid_inner[y_inner][x]
