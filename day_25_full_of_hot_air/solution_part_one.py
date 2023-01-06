
__author__ = "Maximilian Geitner"
__date__ = "25.12.2022"


import numpy as np


def letter_to_value(letter):
    # mapping between character and actual value
    if letter == '2':
        return 2
    elif letter == '1':
        return 1
    elif letter == '0':
        return 0
    elif letter == '-':
        return -1
    elif letter == '=':
        return -2


def add_to_buffer(buf, snafu_number):
    index = 0

    for idx in range(len(snafu_number) - 1, -1, -1):
        letter = snafu_number[idx]
        amount = letter_to_value(letter)
        if len(buf) <= index:
            buf.append(0)
        # print("Val ", letter, amount)
        buf[index] += amount
        index += 1
    return buf


def parse_decimal(snafu_number):
    multiplier = 1
    temp = 0
    for i in range(len(snafu_number) - 1, -1, -1):
        letter = snafu_number[i]
        amount = letter_to_value(letter) * multiplier
        # print("Val ", letter, amount)
        temp += amount
        multiplier *= 5
    return temp


def decimal_to_snafu(decimal):
    result = ""
    # Step 1: Find multiplier and digit that is closest to the decimal number
    mult_pos = 0
    mult = 1
    is_valid = False
    cur_closest_val = '0'
    # cur_min_diff = decimal
    correctable = 0
    remaining = 0
    while not is_valid:
        for letter in ['1', '-', '2', '=']:
            val = letter_to_value(letter)
            cur_val = val * mult
            remaining = decimal - cur_val

            if np.abs(remaining) <= correctable:
                # if absolute remaining value can be corrected by remaining digits, keep value
                # print("Valid", val, cur_val, remaining)
                is_valid = True
                # cur_min_diff = decimal - cur_val
                cur_closest_val = letter
                break
        # print("Mult: ", cur_closest_val, mult, cur_min_diff, correctable)
        if not is_valid:
            mult *= 5
            mult_pos += 1
            if correctable == 0:
                correctable = 2
            else:
                correctable *= 5
                correctable += 2
        if mult_pos > 30:
            print("Error")
            break

    result += cur_closest_val
    # Step 2: Find other digits step by step
    # print("Closest Val", cur_closest_val, mult_pos, remaining)
    if remaining != 0:
        # fill remaining value by using recursion
        result_rec = decimal_to_snafu(remaining)
        # add padding
        while len(result) + len(result_rec) <= mult_pos:
            result += '0'
        return result + result_rec
    else:
        # add padding
        while len(result) <= mult_pos:
            result += '0'
        # reduce remaining sum
        return result


if __name__ == '__main__':
    file = open('input.txt', 'r')

    total = 0
    buffer = []
    # Step 1: Read input
    for line in file:
        line = line.replace("\n", "")
        value = parse_decimal(line)  # translate read sequence to decimal value
        total += value

    # Step 2: Convert decimal value to snafu value
    sol = decimal_to_snafu(total)
    print("Decimal value of total: ", total)
    print("SNAFU number for Bob's console (Solution Part One): ", sol)
