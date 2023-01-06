
__author__ = "Maximilian Geitner"
__date__ = "23.12.2022"

from day_23_unstable_diffusion.elf import Elf
from day_23_unstable_diffusion.helper_functions import find_min_pos, find_max_pos, set_val, get_val

if __name__ == '__main__':
    # constants
    NONE = 0
    PROPOSED = 1
    DENIED = 2
    ELF = 3
    # constants direction
    NORTH = 0
    NW = 1
    NE = 2
    WEST = 3
    EAST = 4
    SOUTH = 5
    SW = 6
    SE = 7
    consideration_order = [NORTH, SOUTH, WEST, EAST]  # north, south, west, east
    # variables
    grid = []
    list_elf_pos = []
    elfs = []

    grid_proposals = []
    row_index = 0

    file = open('input.txt', 'r')

    # Step 1: Read input
    for line in file:
        line = line.replace("\n", "")

        col_index = 0
        for letter in line:
            if letter == '#':
                # elf found
                elfs.append(Elf([row_index, col_index]))
                list_elf_pos.append([row_index, col_index])
            col_index += 1
        row_index += 1
    file.close()

    rounds = 0
    elfs_moved = 0

    while True:
        # Step 2.1: initialize grid
        min_pos = find_min_pos(list_elf_pos)
        max_pos = find_max_pos(list_elf_pos)
        height = max_pos[0] - min_pos[0] + 3  # one tile border
        width = max_pos[1] - min_pos[1] + 3  # one additional border tile
        offset = [-(min_pos[0] - 1), -(min_pos[1] - 1)]
        print("Create Grid...")
        grid_proposals = []
        grid_elfs = []
        for y in range(height):
            grid_proposals.append([NONE] * width)
            grid_elfs.append([NONE] * width)
        # fill grid with elfs
        for elf in elfs:
            set_val(grid_elfs, elf.pos, offset, ELF)

        print("Round ", rounds, "Elfs moved: ", elfs_moved)
        elfs_moved = 0

        elf_moved = False
        # Step 2.2: Check for each elf if there are other elfs nearby
        for e in elfs:
            next_location = e.get_next_position(grid_elfs, offset, consideration_order)
            if next_location is None:
                pass  # do nothing
            else:
                if get_val(grid_proposals, next_location, offset) == DENIED:
                    # don't move there
                    pass
                elif get_val(grid_proposals, next_location, offset) == PROPOSED:
                    # put location to denied location
                    set_val(grid_proposals, next_location, offset, DENIED)
                else:
                    # not yet proposed
                    set_val(grid_proposals, next_location, offset, PROPOSED)

        # Step 2.3: For each proposed position, check for duplicates
        #           --> do nothing when two proposals for the same position occur
        pos_next_round = []
        for e in elfs:
            next_location = e.get_next_pos_cache()
            if next_location is None:
                # Case 1
                pos_next_round.append(e.pos)
                pass  # do nothing
            else:
                # move if in proposed list
                if get_val(grid_proposals, next_location, offset) == PROPOSED:
                    # valid proposal
                    e.pos = next_location
                    elf_moved = True
                    elfs_moved += 1
                    pos_next_round.append(next_location)
                elif get_val(grid_proposals, next_location, offset) == DENIED:
                    # is a denied location
                    pos_next_round.append(e.pos)
                else:
                    print("Error")
        # Step 2.4: Update consideration order
        current_consideration = consideration_order[0]  # change consideration order for all elfs
        consideration_order.pop(0)
        consideration_order.append(current_consideration)
        list_elf_pos = pos_next_round

        # check for solution part two
        if not elf_moved:
            print("Round ", str(rounds + 1), " is the first round where no elf has moved (Solution Part Two)", )
            exit(0)
        else:
            rounds += 1
