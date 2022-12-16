
__author__ = "Maximilian Geitner"
__date__ = "15.12.2022"

from day_15_beacon_exclusion_zone.helper_functions import read_file_input, get_manhattan_dist, is_equal_pos

if __name__ == '__main__':
    FILENAME = 'input.txt'
    # selected_row = 10
    selected_row = 2000000  # 10

    # Step 1: Read file input and find minimum/maximum position and save sensor and beacon position in data structure
    beacons, sensors, min_pos, max_pos = read_file_input(FILENAME)
    # print(min_pos, max_pos)
    # create grid
    grid = []

    # Step 2: Add padding to left and right side of row and generate empty grid row
    amount_cols = max_pos[0] - min_pos[0] + 10000001  # x-coordinate
    offset_x = min_pos[0] - 5000000

    print("Generate grid")
    # only generate one row
    for i in range(amount_cols):
        grid.append(True)

    # Step 3: Apply sensor-beacon-relationship to row
    #         This process can take a few minutes.
    print("Fill in grid")
    for x in range(len(sensors)):
        print((x + 1), "/", len(sensors))
        sensor = sensors[x]
        beacon = beacons[x]
        # for each position within the manhattan-distance and in the selected row,
        # set grid value to False
        # grid value = False --> Position is within a sensor radius
        dist = get_manhattan_dist(sensor, beacon)

        j = selected_row
        for i in range(-dist, dist + 1):
            cur_pos = [i + sensor[0], selected_row, ]  # (x, y)
            idx = i + sensor[0] - offset_x

            if is_equal_pos(sensor, cur_pos):
                # sensor pos
                grid[idx] = False
            elif is_equal_pos(beacon, cur_pos):
                grid[idx] = True
            elif get_manhattan_dist(sensor, cur_pos) <= dist:
                # check whether position is within sensor distance or not
                grid[idx] = False
    # Step 4: Count tiles in row that are not in any sensor range and therefore valid beacon positions
    counter = 0
    for i in range(amount_cols):
        if not grid[i]:
            counter += 1

    print("Invalid Beacon Positions in the selected Row (Solution Part One): ", counter)
