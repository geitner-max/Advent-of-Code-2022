
__author__ = "Maximilian Geitner"
__date__ = "09.12.2022"

from day_09_rope_bridge.position import Pos


def list_contains_pos(list_pos, pos):
    for entry in list_pos:
        if entry.equals(pos):
            return True
    return False


# Idea:
# a) Move head step-by-step
# b) calculate difference between head and tail knot for column and row attribute
# c) If row or column differs by a value of two, check for two possible cases:
#       Case 1: If head and tail are in a different row and column ==> move diagonally
#       Case 2: Otherwise, move vertically or horizontally in order to close the gap
# d) Update list containing all visited locations of the tail

if __name__ == '__main__':

    file = open('input.txt', 'r')
    # initial position on virtual grid, head and tail start on the same position
    pos_head = Pos(0, 0)
    pos_tail = Pos(0, 0)
    # Create list of positions the tail has visited so far
    visited_pos = [Pos(0, 0)]

    for line in file:
        # Each line of input contains a direction and the amount of steps
        parts = line.replace("\n", "").split(" ")
        direction = parts[0]
        amount = int(parts[1])

        for i in range(amount):
            pos_head = pos_head.move_head(direction)
            pos_tail = pos_tail.calc_next_tail_pos(pos_head)
            # add pos_tail to list if it is a new position
            if not list_contains_pos(visited_pos, pos_tail):
                visited_pos.append(pos_tail)

    file.close()
    # Return the amount of visited positions
    print("Amount of visited Tail locations (Solution Part One): ", len(visited_pos))
