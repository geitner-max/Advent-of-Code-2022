
__author__ = "Maximilian Geitner"
__date__ = "07.12.2022"

# helper class for files
# only size attribute is used for this puzzle


class FileNode:

    def __init__(self, name, size):
        self.file_size = size
        self.name = name

    def get_size(self):
        return self.file_size
