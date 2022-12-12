
__author__ = "Maximilian Geitner"
__date__ = "10.12.2022"


if __name__ == '__main__':

    file = open('input.txt', 'r')

    x = 1  # starting value
    cycle = 0
    next_event = 20

    total = 0

    for line in file:
        # line contains either no-operation (costing one cycle) or add-operation (costing two cycles)
        # draw output during each cycle
        # add-operation completes at the end of the second cycle.
        value = 0
        line = line.replace("\n", "")
        if line == "noop":
            cycle += 1
        else:
            parts = line.split(" ")
            value = int(parts[1])
            cycle += 2
        # Part One: compute signal strength
        # Compute value at the 20th, 60th, 100th, ... cycle and add it to the result value
        if cycle >= next_event:
            to_add = next_event * x
            total += to_add
            next_event += 40

        x += value  # complete add-operation after drawing the next character

    print("Sum of signal strengths (Solution Part One): ", total)
