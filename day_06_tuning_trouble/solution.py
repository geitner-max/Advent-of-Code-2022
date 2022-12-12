
__author__ = "Maximilian Geitner"
__date__ = "06.12.2022"


def find_position(input_puzzle, amount_chars):
    pos = 0
    # in each iteration, try to read four different characters starting at index 'pos'
    # if start-of-packet marker has been found, return result with total amount of characters that has been processed
    #   Part One: pos + 4
    #   Part Two: pos + 14
    while True:
        list_temp = []  # list containing unique characters
        for i in range(amount_chars):
            if not input_puzzle[pos + i] in list_temp:
                list_temp.append(input_puzzle[pos + i])
        if len(list_temp) == amount_chars:
            return pos + amount_chars  # if all read characters has been distinct, return result
        else:
            pos += 1  # otherwise continue with an incremented starting position


if __name__ == '__main__':
    file = open('input.txt', 'r')
    line = file.readline()
    file.close()

    # Solution Part One: Four different characters
    sol1 = find_position(line, 4)
    print("Processed Characters for Start-of-Packet marker Part One: ", sol1)

    # Solution Part Two: 14 unique characters
    sol2 = find_position(line, 14)
    print("Processed Characters for Start-of-Packet marker Part Two: ", sol2)
