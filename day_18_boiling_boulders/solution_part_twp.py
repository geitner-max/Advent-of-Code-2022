
__author__ = "Maximilian Geitner"
__date__ = "18.12.2022"


def is_in_list(cur_block, list_blocks):
    for item in list_blocks:
        if cur_block[0] == item[0] and cur_block[1] == item[1] and cur_block[2] == item[2]:
            # print(cur_block, item)
            return True
    return False


def is_in_bounds(entry, min_block, max_block):
    for idx in range(3):
        if entry[idx] < min_block[idx]:
            return False
        elif entry[idx] > max_block[idx]:
            return False
    return True


def get_neighbors_edge(cur, min_block, max_block):
    neighbors = []
    for idx in range(3):
        entry_0 = [cur[0], cur[1], cur[2]]
        entry_0[idx] += 1
        if is_in_bounds(entry_0, min_block, max_block):
            neighbors.append(entry_0)
        entry_1 = [cur[0], cur[1], cur[2]]
        entry_1[idx] -= 1
        if is_in_bounds(entry_1, min_block, max_block):
            neighbors.append(entry_1)
    return neighbors


# Solution idea: Start at an outer air cube and visit all outer air cubes in the boundary of all lava cubes
#                --> For all outer air cubes, count all air-lava-cube connections
if __name__ == '__main__':
    FILENAME = 'input.txt'
    file = open(FILENAME, 'r')

    lava_cubes = []
    # Step 1: Read file
    for line in file:
        line = line.replace("\n", "")
        parts = line.split(",")

        cube_input = []
        for i in parts:
            cube_input.append(int(i))
        lava_cubes.append(cube_input)

    file.close()
    # Step 2: Compute boundary that contains all lava cubes
    min_cube = lava_cubes[0].copy()
    max_cube = lava_cubes[0].copy()

    for cube in lava_cubes:
        for i in range(3):
            min_cube[i] = min(min_cube[i], cube[i] - 1)
            max_cube[i] = max(max_cube[i], cube[i] + 1)
    print("Min and max: ", min_cube, max_cube)
    
    processed = [min_cube]  # contains already processed cubes
    queue = [min_cube]  # contains not yet completely analyzed cubes
    result = 0

    # Step 3: process all cubes and count direct lava cube neighbours of air cubes
    while len(queue) > 0:
        cube_loop = queue.pop()
        # look at neighbors
        # if neighbor is lava block, increase counter (found one surface)
        # otherwise check if processed --> add to queue if not yet processed
        list_neighbors = get_neighbors_edge(cube_loop, min_cube, max_cube)
        for neighbor in list_neighbors:
            if is_in_list(neighbor, lava_cubes):
                # neighbour is a lava cube --> valid exterior surface found --> increase counter
                result += 1
            elif not is_in_list(neighbor, processed):
                # neighbour is a not yet processed air cube
                queue.append(neighbor)
                processed.append(neighbor)

    print("Exterior Surface Area (Solution Part Two): ", result)
