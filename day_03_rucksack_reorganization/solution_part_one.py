
__author__ = "Maximilian Geitner"
__date__ = "03.12.2022"


def get_priority(letter):
    code = ord(letter)
    if ord('a') <= code <= ord('z'):
        return code - ord('a') + 1
    else:
        return code - ord('A') + 27


def get_sum(word):
    # look for items in both components and return priority sum depending on the item type
    # split line into two parts
    first_part = word[0:(len(word) // 2)]
    second_part = word[(len(word) // 2):-1]

    found_components = []
    # For each letter in the first part, look if it exists in the second part
    for char in first_part:
        # avoid duplicate letters
        if second_part.find(char) != -1 and char not in found_components:
            found_components.append(char)

    result = 0
    for char in found_components:
        result += get_priority(char)
    return result


if __name__ == '__main__':
    file = open('input.txt', 'r')
    total = 0
    for line in file:
        total += get_sum(line)
    print("Sum of the priorities: ", total)
