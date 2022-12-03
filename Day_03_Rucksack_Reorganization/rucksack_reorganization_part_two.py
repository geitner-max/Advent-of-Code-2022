
__author__ = "Maximilian Geitner"
__date__ = "03.12.2022"


def get_priority(letter):
    code = ord(letter)
    if ord('a') <= code <= ord('z'):
        return code - ord('a') + 1
    else:
        return code - ord('A') + 27


def get_sum(group1, group2, group3):
    # look for items in all three components and return priority sum depending on the item type

    found_components = []
    # For each letter in the first part, look if it exists in the second part
    for char in group1:
        # avoid duplicate letters
        if group2.find(char) != -1 and group3.find(char) != -1 and char not in found_components and char != '\n':
            found_components.append(char)

    result = 0
    for char in found_components:
        result += get_priority(char)
    return result


if __name__ == '__main__':
    file = open('input.txt', 'r')
    total = 0
    offset = 0
    buffer1 = ""
    buffer2 = ""
    for line in file:
        if offset == 0:
            buffer1 = line
        elif offset == 1:
            buffer2 = line
        else:
            total += get_sum(buffer1, buffer2, line)

        offset = (offset + 1) % 3
    print("Sum of the priorities: ", total)
