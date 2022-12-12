
__author__ = "Maximilian Geitner"
__date__ = "07.12.2022"

from day_07_no_space_left_on_device.file_node import FileNode
from day_07_no_space_left_on_device.node import Node

# Example Commands:
# dir d
# $ cd a
# 123 abc.txt
# Command with no directory/file system change:
# $ ls


if __name__ == '__main__':
    # Initialize variable for root directory and constants
    current_dir = Node("/", None)
    root_dir = current_dir
    TOTAL_SPACE = 70000000
    FREE_SPACE = 30000000

    file = open('input.txt', 'r')
    # Initialize tree structure by executing all commands step-by-step
    for line in file:
        line = line.replace("\n", "")
        parts = line.split(" ")
        if line.startswith("dir"):
            # create new folder in current directory
            current_dir.add_folder(Node(parts[1], current_dir))
        elif line.startswith("$"):
            # process command
            if parts[1] == "ls":
                # do nothing
                pass
            elif parts[1] == "cd":
                # change to specified directory depending on last parameter of the command
                current_dir = current_dir.change_dir(parts[2])
        else:
            # create new file in current directory
            current_dir.add_file(FileNode(parts[1], int(parts[0])))
    file.close()

    # Part One: Sum up all directories with a maximum size of 100000 (subdirectories may be counted multiple times)
    print("Solution of Part One: ", root_dir.get_sum())
    # Part Two: Find the smallest directory to delete, which results in an unused space of 300000, total space is 700000
    all_dirs = root_dir.get_dirs()

    smallest_valid_free_space = TOTAL_SPACE
    selected_dir = root_dir.folder_name
    selected_dir_total = root_dir.total
    # Compute for each directory the remaining free space
    # Remaining free space must be above 300000 and smaller than the current value
    for x in all_dirs:
        free_space_delete = TOTAL_SPACE - root_dir.total + x.total
        if smallest_valid_free_space > free_space_delete >= FREE_SPACE:
            selected_dir = x.folder_name
            smallest_valid_free_space = free_space_delete
            selected_dir_total = x.total
    # Result is the total size of the deleted directory that fulfills all requirements
    print("Result Part Two: ", selected_dir, selected_dir_total)
