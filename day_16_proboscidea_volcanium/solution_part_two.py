import numpy as np


from day_16_proboscidea_volcanium.helper_functions import func_backtrack, read_input, calculate_distances

__author__ = "Maximilian Geitner"
__date__ = "16.12.2022"

# Note: Program runs for about 2-3 minutes.

if __name__ == '__main__':
    FILENAME = 'input.txt'

    # Step 1: Read file input
    dict_valves, important_valves = read_input(FILENAME)
    cur_node = "AA"

    # Step 2: Calculate distances between important valves
    calculate_distances(dict_valves, important_valves, cur_node)

    # Step 3: Create two non-empty subsets of important valves,
    # run both subsets with the backtracking function and sum up total_amount
    # Backtracking function has a time limit of 26 (minutes) instead of 30 (minutes)

    # Example subsets with 4 elements, we need to compare following 7 non-empty subset combinations:
    # [0], [1, 2, 3] (0001)
    # [1], [0, 2, 3] (0010)
    # [2], [0, 1, 3] (0100)
    # [3], [0, 1, 2] (0111) Note: order swapped
    # [0, 1] [2, 3]  (0011)
    # [0, 2] [1, 3]  (0101)
    # [0, 3] [1, 2]  (0110) Note: order swapped
    # --> Generation with binary numbers from 0001 to 1000 (values 0/1 indicate in which subset the item belongs to)
    highest_total = 0
    r1 = []
    r2 = []
    idx = 0
    # from 1 to 2 ^ (valve_count - 1)
    for i in range(1, np.power(2, len(important_valves) - 1)):
        if i % 1000 == 0:
            print((i + 1), "/", np.power(2, len(important_valves) - 1))
        # create binary number that represents subset distribution
        str_bin_num = bin(i)[2:].zfill(len(important_valves))
        subset_0 = []
        subset_1 = []
        # assign valves one of the two subsets
        for x in range(len(str_bin_num)):
            if str_bin_num[x] == '0':
                subset_0.append(important_valves[x])
            else:
                subset_1.append(important_valves[x])
        # print(subset_0, subset_1)
        # create visited list
        visited_0 = [False] * len(subset_0)
        visited_1 = [False] * len(subset_1)
        # call backtrack function
        result_0, r1_cur = func_backtrack(dict_valves, cur_node, subset_0, visited_0, 0, 0, 0, 26)
        result_1, r2_cur = func_backtrack(dict_valves, cur_node, subset_1, visited_1, 0, 0, 0, 26)
        total = result_0 + result_1
        if total > highest_total:
            highest_total = total
            r1 = r1_cur
            r2 = r2_cur
            idx = i
    print("Most achievable Pressure (Solution Part Two): ", highest_total)
    print("Taken routes: ", r1, r2)
    # print(idx)
