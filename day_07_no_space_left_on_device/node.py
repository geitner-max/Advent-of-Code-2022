
__author__ = "Maximilian Geitner"
__date__ = "07.12.2022"

# helper class for folders containing a tree structure and recursive functions


class Node:
    def __init__(self, folder_val, parent):
        self.folder_name = folder_val
        self.files = []
        self.sub_folders = []
        self.parent = parent
        self.total = 0

    # add folder as child to this directory
    def add_folder(self, folder):
        self.sub_folders.append(folder)

    # add file to this directory
    def add_file(self, file_val):
        self.files.append(file_val)

    # either move to root, parent subdirectory
    def change_dir(self, value):
        if value == "..":
            # parent directory
            return self.parent
        elif value == "/":
            # root directory
            if self.parent is None:
                return self
            cur = self.parent
            while cur.parent is not None:
                cur = cur.parent
            return cur
        else:
            # subdirectory
            for x in self.sub_folders:
                if x.folder_name == value:
                    return x

    # return total size of directory, computed by aggregating sizes of subdirectories and all files in this directory
    def get_size(self):
        result = 0
        for x in self.files:
            result += x.get_size()

        for y in self.sub_folders:
            result += y.get_size()
        self.total = result  # save value for part two
        return result

    # function for part one, only aggregating directories with a maximum of 100000
    def get_sum(self):
        total = 0
        # sum up valid sums of all subdirectories
        for child in self.sub_folders:
            total += child.get_sum()
        dir_size = self.get_size()
        if dir_size <= 100000:
            total += dir_size  # add sum of this directory, if it is below 100000
        return total

    # return list of all directories in this or in any subdirectories
    def get_dirs(self):
        result = []
        for child in self.sub_folders:
            result = result + child.get_dirs()
        result.append(self)
        return result
