
__author__ = "Maximilian Geitner"
__date__ = "09.12.2022"


import numpy as np


class Pos:

    # position consists of x- and y-coordinate
    # col = x-pos
    # row = y-pos
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_dist(self, pos):
        return np.abs(self.x - pos.x) + np.abs(self.y - pos.y)

    # method performs one movement step (head movement)
    def move_head(self, direction):
        # values: R, U, L, D
        if direction == 'R':
            return Pos(self.x + 1, self.y)
        elif direction == 'U':
            return Pos(self.x, self.y - 1)
        elif direction == 'L':
            return Pos(self.x - 1, self.y)
        else:
            return Pos(self.x, self.y + 1)

    # Methods calculates next tail or successor knot position
    def calc_next_tail_pos(self, head_pos):
        # calculate row and column difference compared to previous knot
        x_pos_diff = np.abs(head_pos.x - self.x)
        y_pos_diff = np.abs(head_pos.y - self.y)
        x_diff = 1
        y_diff = 1
        if head_pos.x < self.x:
            x_diff = -1
        if head_pos.y < self.y:
            y_diff = -1

        if (x_pos_diff != 0 and y_pos_diff == 2) or (x_pos_diff == 2 and y_pos_diff != 0):
            # Move diagonally
            x_diff = 1
            y_diff = 1
            if head_pos.x < self.x:
                x_diff = -1
            if head_pos.y < self.y:
                y_diff = -1
            return Pos(self.x + x_diff, self.y + y_diff)
        elif x_pos_diff == 2:
            # Move Horizontally (LEFT/RIGHT)
            return Pos(self.x + x_diff, self.y)
        elif y_pos_diff == 2:
            # Move Vertically (UP/DOWN)
            return Pos(self.x, self.y + y_diff)
        else:
            return Pos(self.x, self.y)

    def get_text(self):
        return str(self.x) + ", " + str(self.y)

    # helper method for comparing positions on equality
    def equals(self, pos):
        return self.x == pos.x and self.y == pos.y
