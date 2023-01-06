
__author__ = "Maximilian Geitner"
__date__ = "24.12.2022"

# constants
EMPTY_TILE = 0
WALL_TILE = 1  # Wall or storm in simulation
EXIT_TILE = 2

def print_storm_list(list_storm):
    print(list(map(lambda item: str(item), list_storm)))


def build_grid(grid_base, rows, cols, list_storms):
    grid_current = []
    for j in range(rows):
        grid_temp = []
        for i in range(cols):
            if grid_base[j][i] == WALL_TILE:
                grid_temp.append(WALL_TILE)
            else:
                grid_temp.append(EMPTY_TILE)
        grid_current.append(grid_temp)
    # add storms to grid
    for storm in list_storms:
        grid_current[storm.pos[0]][storm.pos[1]] = WALL_TILE
    return grid_current


def get_next(pos, grid_storms, rows, cols):
    candidates = []
    next_diff = [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]]
    for diff in next_diff:
        next_pos = [pos[0] + diff[0], pos[1] + diff[1]]
        if next_pos[0] >= 0 and next_pos[1] >= 0 and next_pos[0] < rows and next_pos[1] < cols:
            if grid_storms[next_pos[0]][next_pos[1]] == EMPTY_TILE:
                candidates.append(next_pos)
    return candidates


def is_in_list(item, list_pos):
    for entry in list_pos:
        if item[0] == entry[0] and item[1] == entry[1]:
            return True
    return False
