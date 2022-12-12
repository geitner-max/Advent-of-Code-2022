
__author__ = "Maximilian Geitner"
__date__ = "11.12.2022"

from day_11_monkey_in_the_middle.item import Item
from day_11_monkey_in_the_middle.monkey import Monkey

# Solution Idea:
# a) Initialize monkeys similar as in part one,
#   but now items are not controlled by monkeys anymore and instead individual objects with additional attributes.
#   Each item has one value for each monkey and always applies 'Modulo <Test-Divisor>'-operation
#   after each value change. <Test-Divisor> is the value given in the input and always a prime number.
#   Example: '  Test: divisible by 19'
# b) Perform 10000 rounds on each item, steps in one round:
#     i) Perform monkey operation depending on the current position (attribute 'pos'). There is no division by 3, but
#        instead a modulo-operation is applied to keep the numbers small. This step is performed as many times as there
#        are monkeys, the second value for the modulo-operation is different each time.
#     ii) Calculate, whether test is positive or not. The value at the index 'pos' must be zero in this case.
#     iii) Throw item to new pos. If the new position is larger than the current position, repeat the same process for
#           the new position starting at i).
# c) Calculate Monkey business value (similar steps as in part one)
#


if __name__ == '__main__':
    file = open('input.txt', 'r')

    monkeys = []

    state = 0
    operation_op = ''
    operation_val = 0
    test_val = 0
    pos_test = 0
    neg_test = 0

    items_all = []
    divisors = []

    for line in file:
        line = line.replace("\n", "")
        if state == 0:
            # Monkey 0:
            state += 1
        elif state == 1:
            # Starting items
            line = line.replace('  Starting items: ', '')
            parts = line.split(",")
            for part in parts:

                items_all.append(Item(int(part), len(monkeys)))
            state += 1
        elif state == 2:
            # Operation:
            line = line.replace('  Operation: new = ', '')
            parts = line.split(' ')
            operation_op = parts[1]
            if parts[2] == 'old':
                operation_val = None
            else:
                operation_val = int(parts[2])
            state += 1
        elif state == 3:
            # Test:
            line = line.replace('  Test: ', '')
            parts = line.split(' ')
            test_val = int(parts[2])
            divisors.append(test_val)
            state += 1
        elif state == 4:
            line = line.replace('    If true: throw to monkey ', '')
            pos_test = int(line)
            state += 1

        elif state == 5:
            # neg test, create monkey, reset values
            line = line.replace('    If false: throw to monkey ', '')
            neg_test = int(line)
            # create monkey
            monkeys.append(Monkey([], operation_op, operation_val, test_val, pos_test, neg_test))
            state = 6
        elif state == 6:
            # process empty line, reset values
            items = []
            operation_op = ''
            operation_val = 0
            test_val = 0
            pos_test = 0
            neg_test = 0
            state = 0

    ITERATIONS = 10000
    for item in items_all:
        item.init_item(divisors)
    # run 10000 rounds
    for i in range(ITERATIONS):
        for item in items_all:
            item.process_round(monkeys)

    # find two most active monkeys
    monkeys.sort(key=lambda x: x.amount_inspections, reverse=True)

    total = monkeys[0].amount_inspections * monkeys[1].amount_inspections
    print('Amount of Monkey Business (Solution Part Two): ', total)
