
__author__ = "Maximilian Geitner"
__date__ = "21.12.2022"

from day_21_monkey_math.monkey import Monkey

if __name__ == '__main__':
    file = open('input.txt', 'r')

    monkeys_terms = []
    monkeys_number = []
    dict_monkey = {}
    root_item = None

    for line in file:
        line = line.replace("\n", "").replace(":", "")
        parts = list(line.split(" "))
        monkey_id = parts[0]
        # don't add humn to data structure

        if len(parts) == 2:
            # lone number
            # print("P1")
            number = int(parts[1])
            monkey_number = Monkey(parts)
            monkeys_number.append(monkey_number)
            dict_monkey[monkey_id] = monkey_number
        else:
            if monkey_id == 'root':
                root_item = Monkey(parts)
                dict_monkey[monkey_id] = root_item
            else:
                # monkey_pending(parts)
                # add uncompleted monkey
                dict_monkey[monkey_id] = Monkey(parts)

    solution = root_item.compute_result_rec_root(dict_monkey)
    print("Yelled number by the human to pass equality test (Solution Part Two): ", int(solution))
