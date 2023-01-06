
__author__ = "Maximilian Geitner"
__date__ = "21.12.2022"

from day_21_monkey_math.monkey import Monkey

if __name__ == '__main__':
    file = open('input.txt', 'r')

    monkeys_pending = []
    dict_monkey = {}
    # Step 1: Read input, divide monkey into two groups: "known monkey value" and "unknown monkey value"
    for line in file:
        line = line.replace("\n", "").replace(":", "")
        parts = list(line.split(" "))
        monkey_id = parts[0]

        if len(parts) == 2:
            # lone number
            number = int(parts[1])
            dict_monkey[monkey_id] = Monkey(parts)
        else:
            # add uncompleted monkey
            monkeys_pending.append(Monkey(parts))
            pass
    # Step 2: for each incomplete term, try to complete arithmetic operation
    #         Stop when the 'root' monkey result has been computed
    while 'root' not in dict_monkey:
        # do next iteration
        monkeys_pending_next = []
        for monkey in monkeys_pending:
            ret_val = monkey.compute_result(dict_monkey)
            if ret_val:
                # completed
                dict_monkey[monkey.monkey_id] = monkey
            else:
                # still uncompleted
                monkeys_pending_next.append(monkey)

    print("Yelled Number by 'root'-monkey (Solution Part One): ", int(dict_monkey['root'].value))
