
__author__ = "Maximilian Geitner"
__date__ = "24.12.2022"

class Storm:
    def __init__(self, initial_pos, direction):
        # constants
        self.EAST = 0
        self.SOUTH = 1
        self.WEST = 2
        self.NORTH = 3
        self.EMPTY_TILE = 0
        self.WALL_TILE = 1  # Wall or storm in simulation
        # translate direction to int
        self.direction = self.dir_to_int(direction)
        self.pos = initial_pos

    def get_dir_vec(self, direction):
        if direction == self.EAST:
            return [0, 1]
        elif direction == self.SOUTH:
            return [1, 0]
        elif direction == self.WEST:
            return [0, -1]
        elif direction == self.NORTH:
            return [-1, 0]
        else:
            return None

    def apply_dir_vec(self, cur_pos, dir_vec):
        return [cur_pos[0] + dir_vec[0], cur_pos[1] + dir_vec[1]]
    def move_pos(self, cur_pos, direction):
        dir_vec = self.get_dir_vec(direction)
        return self.apply_dir_vec(cur_pos, dir_vec)
    def get_val(self, pos, grid_walls):
        return grid_walls[pos[0]][pos[1]]

    def move_one_step(self, amount_rows, amount_cols, grid_walls):
        next_pos = self.move_pos(self.pos, self.direction)
        if self.get_val(next_pos, grid_walls) == self.EMPTY_TILE:
            # next position is valid
            self.pos = next_pos
        else:
            # invert direction vector and move in opposite direction
            # stop at position before wall
            reverse_dir = [-self.get_dir_vec(self.direction)[0], -self.get_dir_vec(self.direction)[1]]
            cur_pos = self.pos
            next_pos = self.apply_dir_vec(cur_pos, reverse_dir)
            while self.get_val(next_pos, grid_walls) == self.EMPTY_TILE:
                # if next pos is empty, move one step forward
                cur_pos = next_pos
                next_pos = self.apply_dir_vec(cur_pos, reverse_dir)

            # set cur_pos as new position
            # print(self.pos, "-->", cur_pos, reverse_dir)
            self.pos = cur_pos

    def __str__(self):
        return str(self.pos) + ", " + str(self.direction)


    def dir_to_int(self, letter):
        if letter == '>':
            # east
            return self.EAST
        elif letter == 'v':
            return self.SOUTH
        elif letter == '<':
            return self.WEST
        elif letter == '^':
            return self.NORTH
        else:
            return None