import numpy as np


__author__ = "Maximilian Geitner"
__date__ = "15.12.2022"


def get_min_pos(tuple_pos, cur_min):
    return [min(tuple_pos[0], cur_min[0]), min(tuple_pos[1], cur_min[1])]


def get_max_pos(tuple_pos, cur_max):
    return [max(tuple_pos[0], cur_max[0]), max(tuple_pos[1], cur_max[1])]


def get_manhattan_dist(pos1, pos2):
    return np.abs(pos1[0] - pos2[0]) + np.abs(pos1[1] - pos2[1])


def is_equal_pos(pos1, pos2):
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]


def read_file_input(filename):
    file = open(filename, 'r')
    sensors = []
    beacons = []
    min_pos = [0, 0]
    max_pos = [0, 0]

    for line in file:
        # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        line_2 = line.replace("\n", "").replace("Sensor at ", "")\
            .replace(": closest beacon is at ", " ").replace(",", "")
        parts = line_2.split(" ")
        # print(parts)
        # Sensor
        x1 = int(parts[0].replace("x=", ""))
        y1 = int(parts[1].replace("y=", ""))
        # Corresponding nearest beacon
        x2 = int(parts[2].replace("x=", ""))
        y2 = int(parts[3].replace("y=", ""))
        # print(x1, y1, "|", x2, y2)
        sensor_pos = [x1, y1, ]
        beacon_pos = [x2, y2, ]
        sensors.append(sensor_pos)
        beacons.append(beacon_pos)
        min_pos = get_min_pos(sensor_pos, min_pos)
        min_pos = get_min_pos(beacon_pos, min_pos)
        max_pos = get_max_pos(sensor_pos, max_pos)
        max_pos = get_max_pos(beacon_pos, max_pos)
    file.close()
    return beacons, sensors, min_pos, max_pos
