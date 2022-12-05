__author__ = "Maximilian Geitner"
__date__ = "05.12.2022"

if __name__ == '__main__':
    file = open('input.txt', 'r')

    stacks = []

    stack_temp = []
    read_state = 0
    amount_stacks = 0

    for line in file:

        if read_state == 0:
            # read all lines until line containing digits appears "1   2   3   ..."
            if line.find("1") != -1:
                # line with amount of stacks
                # create stacks
                read_state = 1
                amount_stacks = len(line)//4
                # create entry for each stack
                for i in range(amount_stacks):
                    stacks.append([])
                # add empty list for each stack and fill up with values
                while not len(stack_temp) == 0:
                    current_line = stack_temp.pop()
                    for i in range(amount_stacks):
                        value = current_line[i * 4:i * 4 + 3]  # add value to stack e.g. "[A] " or "    "
                        if value != "   ":
                            stacks[i].append(value)
            else:
                #read input line by line
                stack_temp.append(line)
        elif read_state == 1:
            # skip empty line in the input.txt file
            read_state = 2
        elif read_state == 2:
            # process move commands line by line
            # preprocess line
            line = line.replace("move ", "").replace("from ", "").replace("to ", "")
            # extract amount of values to move, start and destination stack of transfer
            parts = line.split(" ")
            amount = int(parts[0])
            start = int(parts[1]) - 1
            dest = int(parts[2]) - 1
            # move value one by one
            for i in range(amount):
                value = stacks[start].pop()
                stacks[dest].append(value)

        # at the end, look at top crate in each stack
        result = ""
        for i in range(amount_stacks):
            if len(stacks[i]) != 0:
                value = stacks[i][-1]
                result += value[1:2]
    # print result, top value of each stack concatenated
    print("Solution: ", result)
