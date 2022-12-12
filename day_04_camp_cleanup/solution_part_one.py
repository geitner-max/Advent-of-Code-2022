__author__ = "Maximilian Geitner"
__date__ = "04.12.2022"

if __name__ == '__main__':
    file = open('input.txt', 'r')

    total = 0

    for line in file:
        # read both intervals from file
        parts = line.split(",")
        range1 = parts[0].split("-")
        min1 = int(range1[0])
        max1 = int(range1[1])

        range2 = parts[1].split("-")
        min2 = int(range2[0])
        max2 = int(range2[1])
        # check if one interval fully overlaps with the other
        if min1 >= min2 and max1 <= max2:
            total += 1
        elif min2 >= min1 and max2 <= max1:
            total += 1

    print("Amount of pairs that fully overlap: ", total)
