
__author__ = "Maximilian Geitner"
__date__ = "23.12.2022"

from day_23_unstable_diffusion.helper_functions import get_val


class Elf:

    def __init__(self, pos):
        # constants
        self.NORTH = 0
        self.NW = 1
        self.NE = 2
        self.WEST = 3
        self.EAST = 4
        self.SOUTH = 5
        self.SW = 6
        self.SE = 7
        self.ELF = 3

        self.pos = pos
        # self.consideration_order = [self.NORTH, self.SOUTH, self.WEST, self.EAST]
        self.cache_pos = None
        self.cache_dir = None

    def get_next_pos(self, direction):
        pos_compare = self.pos.copy()
        if direction == self.NORTH or direction == self.NW or direction == self.NE:
            # y - 1
            pos_compare[0] -= 1
        elif direction == self.SOUTH or direction == self.SW or direction == self.SE:
            pos_compare[0] += 1
        if direction == self.WEST or direction == self.NW or direction == self.SW:
            # x - 1
            pos_compare[1] -= 1
        elif direction == self.EAST or direction == self.NE or direction == self.SE:
            pos_compare[1] += 1
        return pos_compare

    def is_elf_nearby_dir(self, direction, grid_elfs, grid_offset):
        pos_compare = self.get_next_pos(direction)
        if get_val(grid_elfs, pos_compare, grid_offset) == self.ELF:
            return True
        return False

    def is_elf_nearby(self, grid_elfs, grid_offset):
        # pos_to_check = [self.NORTH, self.NW, self.NE, self.SOUTH, self.SW, self.SE, self.WEST, self.EAST]
        cur_pos = self.pos
        for y_diff in range(-1, 2, 1):
            for x_diff in range(-1, 2, 1):
                if y_diff != 0 or x_diff != 0:
                    next_pos = [cur_pos[0] + y_diff, cur_pos[1] + x_diff]
                    if get_val(grid_elfs, next_pos, grid_offset) == self.ELF:
                        return True
        return False

    def get_next_position(self, grid_elfs, grid_offset, current_consideration):
        if not self.is_elf_nearby(grid_elfs, grid_offset):
            # Case 1: No elfs nearby --> do nothing
            self.cache_pos = None

            return None
            # Case 2: One direction is free --> propose this position
        else:
            # check for possible next location
            next_location = None
            for consideration in current_consideration:
                if consideration == self.NORTH and not (self.is_elf_nearby_dir(self.NORTH, grid_elfs, grid_offset)
                                                        or self.is_elf_nearby_dir(self.NW, grid_elfs, grid_offset)
                                                        or self.is_elf_nearby_dir(self.NE, grid_elfs, grid_offset)):
                    next_location = self.get_next_pos(self.NORTH)
                    break
                elif consideration == self.SOUTH and not (
                        self.is_elf_nearby_dir(self.SOUTH, grid_elfs, grid_offset)
                        or self.is_elf_nearby_dir(self.SW, grid_elfs, grid_offset)
                        or self.is_elf_nearby_dir(self.SE, grid_elfs, grid_offset)):
                    next_location = self.get_next_pos(self.SOUTH)
                    break
                elif consideration == self.WEST and not (
                        self.is_elf_nearby_dir(self.WEST, grid_elfs, grid_offset) or self.is_elf_nearby_dir(self.SW,
                                                                                                            grid_elfs,
                                                                                                            grid_offset)
                        or self.is_elf_nearby_dir(self.NW, grid_elfs, grid_offset)):
                    next_location = self.get_next_pos(self.WEST)
                    break
                elif consideration == self.EAST and not (
                        self.is_elf_nearby_dir(self.EAST, grid_elfs, grid_offset) or self.is_elf_nearby_dir(self.SE,
                                                                                                            grid_elfs,
                                                                                                            grid_offset)
                        or self.is_elf_nearby_dir(self.NE, grid_elfs, grid_offset)):
                    next_location = self.get_next_pos(self.EAST)
                    break
            if next_location is None:
                self.cache_pos = None
            else:
                self.cache_pos = next_location.copy()
            return next_location

    def get_next_pos_cache(self):
        return self.cache_pos
