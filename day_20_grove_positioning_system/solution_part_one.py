
__author__ = "Maximilian Geitner"
__date__ = "20.12.2022"

from day_20_grove_positioning_system.helper_functions import find_item, move_forward, move_backward

if __name__ == '__main__':
    file = open('input.txt', 'r')

    numbers = []
    idx = 0
    # Step 1: Read file
    for line in file:
        line = line.replace("\n", "")
        numbers.append([int(line), idx])
        idx += 1

    file.close()
    amount_items = len(numbers)

    # Step 2: Simulate scenario
    for idx in range(amount_items):
        # find position in list
        current_idx = find_item(idx, numbers)
        value = numbers[current_idx][0]
        # move amount of positions in list
        if value >= 0:
            for y in range(value):
                current_idx, numbers = move_forward(current_idx, numbers)
        else:
            for y in range(-value):
                current_idx, numbers = move_backward(current_idx, numbers)

    # Step 3 : Compute Sum of Grove Coordinates
    state = 0
    current_idx = 0
    total = 0
    for idx in range(len(numbers)):
        val, _ = numbers[idx]
        if val == 0:
            # found start
            current_idx = idx
            break
    pos_to_check = [(current_idx + 1000) % amount_items, (current_idx + 2000) % amount_items,
                    (current_idx + 3000) % amount_items]
    for idx in pos_to_check:
        total += numbers[idx][0]
    print("Sum of the Three Numbers that form the Grove Coordinates (Solution Part One): ", total)
