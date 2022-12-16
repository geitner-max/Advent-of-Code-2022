
from day_16_proboscidea_volcanium.helper_functions import func_backtrack, read_input, calculate_distances

__author__ = "Maximilian Geitner"
__date__ = "16.12.2022"


if __name__ == '__main__':
    FILENAME = 'input.txt'

    # Step 1: Read file input
    dict_valves, important_valves = read_input(FILENAME)
    cur_node = "AA"
    # Step 2: Calculate distances between important valves (flow_rate > 0)
    calculate_distances(dict_valves, important_valves, cur_node)

    # Step 3: Find most promising route via backtracking and time limit of 30 (minutes)
    visited = [False] * len(important_valves)
    result, route = func_backtrack(dict_valves, cur_node, important_valves, visited, 0, 0, 0, 30)
    print("Most achievable pressure (Solution Part One): ", result)
    print("Route taken: ", route)
