
__author__ = "Maximilian Geitner"
__date__ = "20.12.2022"


def find_item(index, numbers):
    for i in range(len(numbers)):
        value, start_idx = numbers[i]
        if start_idx == index:
            return i
    return -1


def move_forward(idx, numbers):
    # move one position forward
    next_index = (idx + 1) % len(numbers)
    # save current value
    first_val, index = numbers[idx]
    numbers[idx] = [numbers[next_index][0], numbers[next_index][1]]
    numbers[next_index] = [first_val, index]
    return next_index, numbers


def move_backward(idx, numbers):
    # move one position forward
    next_index = idx - 1
    if next_index < 0:
        next_index = len(numbers) - 1
    # save current value
    first_val, index = numbers[idx]
    numbers[idx] = [numbers[next_index][0], numbers[next_index][1]]
    numbers[next_index] = [first_val, index]
    return next_index, numbers
