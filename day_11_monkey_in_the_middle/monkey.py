
__author__ = "Maximilian Geitner"
__date__ = "11.12.2022"


class Monkey:

    def __init__(self, items, operation_op, operation_val, test_div, pos_test, neg_test):
        self.amount_inspections = 0     # value counting how often a monkey looked at an item
        self.items = items              # list containing the items the monkey holds
        self.operation_op = operation_op    # binary-operator, '+' or '*'
        self.operation_val = operation_val  # second value, either a specified number of None
        # meaning None: use first value again, e.g. for value * value
        self.test_div = test_div            # number, is a prime number
        self.pos_test_monkey = pos_test     # index of monkey that receives item after a positive test result
        self.neg_test_monkey = neg_test     # index of monkey that receives item after a negative test result

    def comp_worry_level(self, value):
        temp = self.operation_val
        if self.operation_val is None:
            temp = value

        if self.operation_op == '*':
            value = value * temp
        elif self.operation_op == '+':
            value = value + temp
        else:
            print("Error: ", self.operation_op , " not supported")
            return value

        value = value // 3
        return value

    def process_round(self, monkeys):
        # increment counter for amount of items that are processed
        self.amount_inspections += len(self.items)
        # compute new worry level and divide by three
        self.items = list(map(self.comp_worry_level, self.items))

        # test items and throw them to other monkeys
        for item in self.items:
            if item % self.test_div == 0:
                # positive test
                monkeys[self.pos_test_monkey].items.append(item)
            else:
                # negative test
                monkeys[self.neg_test_monkey].items.append(item)
        self.items = []  # all items have been thrown out, reset list

