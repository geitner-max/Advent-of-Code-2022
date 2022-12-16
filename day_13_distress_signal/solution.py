
__author__ = "Maximilian Geitner"
__date__ = "13.12.2022"

# constants for list comparison
RIGHT_ORDER = 0
NOT_RIGHT_ORDER = 1
SIMILAR = 2


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def is_list(input_l):
    return isinstance(input_l, list)


def parse_list(input_line):
    result = []
    # remove first and last letter
    input_line = input_line[1:-1]

    # split by comma, only on first level
    level = 0
    current_input = ""
    for letter in input_line:
        # split result
        if letter == ',' and level == 0:
            if is_integer(current_input):
                result .append(int(current_input))
            else:
                # print("Parse again: ", current_input)
                result.append(parse_list(current_input))
            current_input = ""
        elif letter == '[':
            current_input += '['
            level += 1
        elif letter == ']':
            current_input += ']'
            level -= 1
        else:
            current_input += letter
    # add last read input to result
    if current_input != "":
        if is_integer(current_input):
            result.append(int(current_input))
        else:
            result.append(parse_list(current_input))

    return result


def is_right_order(list1, list2):
    # compare each item on left side with corresponding right side item
    for i in range(len(list1)):
        if len(list2) == i:
            # right side runs out of items to compare
            return NOT_RIGHT_ORDER
        item1 = list1[i]
        item2 = list2[i]
        # compare items with the same index from both lists
        if not is_list(item1) and not is_list(item2):
            # Two Integers
            if int(item1) > int(item2):
                # Left value is bigger than right value
                return NOT_RIGHT_ORDER
            elif int(item1) < int(item2):
                # Left value is smaller than right value
                return RIGHT_ORDER
        elif is_list(item1) and is_list(item2):
            # both items are lists, recursive function call
            res = is_right_order(item1, item2)
            if res != SIMILAR:
                return res
        elif is_list(item2):
            # right side is a list
            # convert mixed types and recursively evaluate order
            res = is_right_order([item1], item2)
            if res != SIMILAR:
                return res
        elif is_list(item1):
            # left side is a list
            # convert mixed types and recursively evaluate order
            res = is_right_order(item1, [item2])
            if res != SIMILAR:
                return res
        else:
            print("Error")

    # if all individual items are in the right order and left list is shorter than right list
    # Note: Case Right list has more elements than left list is covered within the loop
    if len(list1) < len(list2):
        return RIGHT_ORDER
    else:
        # otherwise they are similar
        return SIMILAR


if __name__ == '__main__':
    file = open('input.txt', 'r')

    state = 0
    pair_index = 1
    l1 = []
    l2 = []
    total_indices = 0
    lists = [[2], [6]]  # for part two, initialization of divider packets

    for line in file:
        line = line.replace("\n", "")
        if state == 0:
            # first list
            l1 = parse_list(line)
            lists.append(l1)
            state = 1
        elif state == 1:
            # second list
            l2 = parse_list(line)
            lists.append(l2)
            state = 2
            # compare lists, for part one
            is_list_right_order = is_right_order(l1, l2)
            if is_list_right_order != NOT_RIGHT_ORDER:
                # sum up indices of pairs in the right order
                total_indices += pair_index
        else:
            # process empty line
            state = 0
            pair_index += 1

    # Part one: Print amount of pairs in the right order
    print("Sum of indices (Solution Part One): ", total_indices)

    # Part Two: Sort all lists by the right order and find markers in the sorted list
    lists_ordered = []
    # idea: Pick the lowest value from list and transfer it to lists_ordered
    #       Repeat process until no item is left in lists

    while len(lists) > 0:
        smallest_item = lists[0]
        index = 0
        for idx in range(1, len(lists)):
            if is_right_order(smallest_item, lists[idx]) == NOT_RIGHT_ORDER:
                # print("Found smaller list")
                smallest_item = lists[idx]
                index = idx
        # after iteration, transfer list
        lists_ordered.append(smallest_item)
        lists.remove(smallest_item)

    # find divider keys in lists and use position for computing the decoder key
    decoder_key = 1
    for idx in range(len(lists_ordered)):
        item = lists_ordered[idx]
        if item == [6]:
            decoder_key *= (idx + 1)
            # print("FOUND: ", i + 1)
        elif item == [2]:
            decoder_key *= (idx + 1)
            # print("Found: ", i + 1)

    print("Decoder Key (Solution Part Two): ", decoder_key)
