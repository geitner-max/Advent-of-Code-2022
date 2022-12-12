
__author__ = "Maximilian Geitner"
__date__ = "11.12.2022"


class Item:

    def __init__(self, value, pos):
        self.value = value
        self.values = []
        self.divisor = []
        self.pos = pos

    def init_item(self, divisor):
        # init test div for each monkey and initialize values
        self.divisor = divisor

        for div in self.divisor:
            self.values.append(self.value % div)

    def apply_op(self, op, val):
        for i in range(len(self.values)):
            if val is None:
                # take current value
                if op == '+':
                    self.values[i] = (self.values[i] + self.values[i]) % self.divisor[i]
                elif op == '*':
                    self.values[i] = (self.values[i] * self.values[i]) % self.divisor[i]
                else:
                    print("Error: ", op, val)
            else:
                if op == '+':
                    self.values[i] = (self.values[i] + val) % self.divisor[i]
                elif op == '*':
                    self.values[i] = (self.values[i] * val) % self.divisor[i]
                else:
                    print("Error: ", op, val)

    def process_round(self, monkeys):
        stay_in_loop = True
        while stay_in_loop:
            # operation
            self.apply_op(monkeys[self.pos].operation_op, monkeys[self.pos].operation_val)

            pos = monkeys[self.pos].neg_test_monkey
            # test, value has value zero
            if self.values[self.pos] == 0:
                # positive result
                pos = monkeys[self.pos].pos_test_monkey
            # throw item
            monkeys[self.pos].amount_inspections += 1
            stay_in_loop = self.pos < pos  # leave loop, if next value is smaller than current value
            self.pos = pos

