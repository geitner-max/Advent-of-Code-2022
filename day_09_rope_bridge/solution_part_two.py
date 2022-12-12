
__author__ = "Maximilian Geitner"
__date__ = "09.12.2022"

from day_09_rope_bridge.position import Pos


def list_contains_pos(list_pos, pos):
    for entry in list_pos:
        if entry.equals(pos):
            return True
    return False


# Idea:
# Data structure consists of one head knot (following the input) and 9 successor knots.
# The last knot is the tail knot that needs to be tracked for the solution.
#
# a) Move head step-by-step
# b) Move each successor knot similar to part one:
#   i) calculate difference between one knot and their successor knot for column and row attribute
#   ii) If row or column differs by a value of two, check for two possible cases:
#           Case 1: If head and tail are in a different row and column ==> move diagonally
#           Case 2: Otherwise, move vertically or horizontally in order to close the gap
# c) Update list containing all visited locations of the tail


if __name__ == '__main__':

    file = open('input.txt', 'r')

    pos_head = Pos(0, 0)
    pos_tails = [Pos(0, 0)] * 9  # ten entries for tail

    visited_pos = [Pos(0, 0)]

    for line in file:
        # read direction and amount of steps from input file
        parts = line.replace("\n", "").split(" ")
        direction = parts[0]
        amount = int(parts[1])

        for i in range(amount):
            # a) Move head
            pos_head = pos_head.move_head(direction)
            # b) Move first successor knot
            pos_tails[0] = pos_tails[0].calc_next_tail_pos(pos_head)

            # Move remaining knots
            for j in range(1, 9):
                pos_tails[j] = pos_tails[j].calc_next_tail_pos(pos_tails[j - 1])
            # c) Update tail knot visited locations
            if not list_contains_pos(visited_pos, pos_tails[8]):
                visited_pos.append(pos_tails[8])
    file.close()
    print("Amount of Tail Knot Visited Locations (Solution Part Two): ", len(visited_pos))
