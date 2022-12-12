
__author__ = "Maximilian Geitner"
__date__ = "11.12.2022"

from day_11_monkey_in_the_middle.monkey import Monkey


# Solution Idea:
# a) Create all monkeys given in the input
# b) Simulate 20 rounds of monkey throwing and count for each monkey the amount of inspected items
#       For each monkey in each iteration:
#           i) Apply operation on each item (including division by 3)
#           ii) Calculate value for test
#           iii) Depending on test, throw it to the next specified monkey
# c) Find the two highest amounts and calculate solution for part one
if __name__ == '__main__':
    file = open('input.txt', 'r')

    monkeys = []

    state = 0
    items = []
    operation_op = ''
    operation_val = 0
    test_val = 0
    pos_test = 0
    neg_test = 0

    # Read monkey information line-by-line, each line contains different kinds of information
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
                items.append(int(part))
            state += 1
        elif state == 2:
            # Operation
            line = line.replace('  Operation: new = ', '')
            parts = line.split(' ')
            operation_op = parts[1]
            # second bin-op value is None, if the first bin-op is used twice
            if parts[2] == 'old':
                operation_val = None
            else:
                # parse given number
                operation_val = int(parts[2])
            state += 1
        elif state == 3:
            # Test:
            line = line.replace('  Test: ', '')
            parts = line.split(' ')
            test_val = int(parts[2])
            state += 1
        elif state == 4:
            # If true:
            line = line.replace('    If true: throw to monkey ', '')
            pos_test = int(line)
            state += 1

        elif state == 5:
            # If false:
            # neg test, create monkey, reset values
            line = line.replace('    If false: throw to monkey ', '')
            neg_test = int(line)
            # create monkey object
            monkeys.append(Monkey(items, operation_op, operation_val, test_val, pos_test, neg_test))
            state = 6
        elif state == 6:
            # process empty line
            items = []
            operation_op = ''
            operation_val = 0
            test_val = 0
            pos_test = 0
            neg_test = 0
            state = 0
    # simulate 20 rounds
    for x in range(20):
        for i in range(len(monkeys)):
            monkeys[i].process_round(monkeys)  # process one round at a specified monkey

    # find two most active monkeys
    monkeys.sort(key=lambda z: z.amount_inspections, reverse=True)
    # print(monkeys[0].amount_inspections)
    # print(monkeys[1].amount_inspections)

    total = monkeys[0].amount_inspections * monkeys[1].amount_inspections

    print('Level of Monkey Business (Solution Part One): ', total)
