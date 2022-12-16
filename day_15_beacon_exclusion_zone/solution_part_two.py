import numpy as np


__author__ = "Maximilian Geitner"
__date__ = "15.12.2022"

from day_15_beacon_exclusion_zone.helper_functions import read_file_input, get_manhattan_dist

if __name__ == '__main__':
    FILENAME = 'input.txt'
    amount_rows = 4000000 + 1  # y-coordinate
    amount_cols = 4000000 + 1  # x-coordinate
    # FILENAME = 'test.txt'
    # amount_rows = 21
    # amount_cols = 21

    # Step 1: Read file input and find minimum/maximum position and save sensor and beacon position in data structure
    beacons, sensors, min_pos, max_pos = read_file_input(FILENAME)
    # Step 2: Compute manhattan-distances for each sensor-beacon-pair
    distances = []
    for i in range(len(beacons)):
        sensor_pos = sensors[i]
        beacon_pos = beacons[i]
        distances.append(get_manhattan_dist(sensor_pos, beacon_pos))
    # Step 3: Find candidates for beacon-position, Distance to sensor = distance + 1
    #         For each candidate, check whether within distance to any other sensor
    #         If no sensor near enough, the candidate is a valid solution
    for x in range(len(sensors)):
        sensor = sensors[x]
        beacon = beacons[x]
        dist = get_manhattan_dist(sensor, beacon) + 1
        points_to_check = []

        start_row = max(0, sensor[1] - dist)
        end_row = min(amount_rows, sensor[1] + dist + 1)

        print("Calculate point list... ", (x + 1), "/", len(sensors))

        for j in range(start_row, end_row):
            # calculate one or two points
            remaining_columns = dist - np.abs(j - sensor[1])
            if remaining_columns == 0:
                # one point
                points_to_check.append((sensor[0], j,))
            else:
                # two points to check
                if sensor[0] - remaining_columns >= 0:
                    points_to_check.append((sensor[0] - remaining_columns, j,))
                if sensor[0] + remaining_columns < amount_cols:
                    points_to_check.append((sensor[0] + remaining_columns, j,))
        print("Check points... ", (x + 1), "/", len(sensors))
        # check all points
        for point in points_to_check:
            is_solution = True
            for y in range(len(sensors)):
                dist_sensor = distances[y]
                if get_manhattan_dist(sensors[y], point) <= dist_sensor:
                    is_solution = False
                    break
            if is_solution:
                print("Position of distress beacon: ", point)
                # Warning: solution is too big for normal python floats with 32 bits
                tuning_frequency = np.float64(np.float64(point[0]) * np.float64(4000000) + np.float64(point[1]))
                sol_str = tuning_frequency.astype(str)
                print("Tuning frequency (Solution Part Two): ", sol_str)
                # solution found: exit program
                exit(0)
