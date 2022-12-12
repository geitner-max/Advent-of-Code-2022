
__author__ = "Maximilian Geitner"
__date__ = "12.12.2022"

import numpy as np


# Solution idea:
# a) Each tile is a node in a graph
# b) There is an edge between two nodes, if the vehicle can move from one tile to its neighbouring tile.
# ==> Perform Dijkstra-algorithm in order to find the shortest path between start and destination node


# vehicle can only climb one position higher, but any amounts of positions lower
# method defines edges between tiles


def can_move(current_letter, next_letter):
    if current_letter == 'S':
        current_letter = 'a'
    elif current_letter == 'E':
        current_letter = 'z'
    if next_letter == 'S':
        next_letter = 'a'
    elif next_letter == 'E':
        next_letter = 'z'
    val = ord(current_letter)
    val2 = ord(next_letter)
    # check for difference of 1
    if val2 > val:
        return np.abs(val - val2) <= 1
    else:
        return True


def dijkstra(grid_elevation, current_node, current_dist, queue, bounds, destination):
    # init grid with not visited values
    grid_visited = []
    for rows in grid_elevation:
        current_row = []
        for _ in rows:
            current_row.append(False)
        grid_visited.append(current_row)
    # start pos is already visited
    grid_visited[current_node[0]][current_node[1]] = True
    while True:
        # print(current_node, "Distance: ", current_dist)
        if current_node[0] == destination[0] and current_node[1] == destination[1]:
            # end reached
            return current_dist

        # Step 1) for current node: add neighbouring tiles to queue, if not yet visited
        # if neighbouring tile in queue, update distance and predecessor
        # Step 2: visit value in queue with lowest destination
        for x in range(4):
            next_row = current_node[0]
            next_column = current_node[1]
            # look in each direction
            if x == 0:
                next_row -= 1
            elif x == 1:
                next_row += 1
            elif x == 2:
                next_column += 1
            elif x == 3:
                next_column -= 1
            # check valid field and height difference
            if bounds[0] > next_row >= 0 and bounds[1] > next_column >= 0 \
                    and can_move(grid_elevation[current_node[0]][current_node[1]],
                                 grid_elevation[next_row][next_column]):
                # check field for visited attribute
                if not grid_visited[next_row][next_column]:
                    # add to queue
                    grid_visited[next_row][next_column] = True
                    queue.append([next_row, next_column, current_node, current_dist + 1])
                else:
                    # tile marked as visited ==> Update tile in queue if it exists (not yet visited)
                    for y in range(len(queue)):
                        (r, c, _, dist) = queue[y]
                        if r == next_row and c == next_row:
                            # update value
                            if dist > current_dist + 1:
                                # shorter route found, update information about dist and predecessor
                                queue[y][2] = current_node
                                queue[y][3] = current_dist + 1
                                break
        # update neighbouring tiles done, do recursive call with the lowest next tile
        if not queue:
            # if no element in queue ==> no route found ==> return None
            return None
        queue.sort(key=lambda z: z[3],)
        picked_node = queue[0]
        dist_next = picked_node[3]
        next_node_pos = (picked_node[0], picked_node[1],)
        del queue[0]
        current_node = next_node_pos
        current_dist = dist_next


if __name__ == '__main__':
    file = open('input.txt', 'r')

    grid = []  # each entry: (letter, visited)
    start_pos_list = []  # contains valid start positions for part two
    start_pos = (0, 0)  # first value is row index, second column index
    dest_pos = (0, 0)

    i = 0  # column
    j = 0  # row
    total_cols = None
    total_rows = 0
    for line in file:
        line = line.replace("\n", "")
        total_rows += 1
        if total_cols is None:
            total_cols = len(line)
        i = 0

        row = []
        for letter in line:
            row.append(letter)
            if letter == 'S':
                start_pos = (j, i,)
                start_pos_list.append((j, i,))
            elif letter == 'a':
                start_pos_list.append((j, i,))
            elif letter == 'E':
                dest_pos = (j, i,)
            i += 1  # inc column
        grid.append(row)
        j += 1

    bounds_grid = (total_rows, total_cols,)

    route = dijkstra(grid, start_pos, 0, [], bounds_grid, dest_pos)
    print('Distance between Start and Destination Position (Solution Part One): ', route)
    # Part Two:
    min_value = None
    for pos in start_pos_list:
        route_dist = dijkstra(grid, pos, 0, [], bounds_grid, dest_pos)
        if route_dist is not None:
            if min_value is None:
                min_value = route_dist
            else:
                min_value = min(min_value, route_dist)
    print('Shortest Distance between a valid Start Position to the Destination (Solution Part Two): ', min_value)
