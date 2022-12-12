
__author__ = "Maximilian Geitner"
__date__ = "01.12.2022"


if __name__ == '__main__':
    file = open('input.txt', 'r')
    current_calories = 0
    list_calories = []
    # code similar to part one, but calories for each person are added to a list and later analyzed
    for line in file:
        # reset counter, if empty line detected
        if line == "\n":
            list_calories.append(current_calories)
            current_calories = 0
        else:
            # increase current counter and compare with current maximum
            current_calories += int(line)
    # add final person to list
    list_calories.append(current_calories)
    file.close()

    # find the three largest values (without sorting the list)
    sum_top_three = 0
    # for each iteration, find the largest value in the list, add it to the sum and remove found value from list
    for i in range(3):
        index_max = 0
        cur_max = 0
        # find current maximum
        for (idx, value) in enumerate(list_calories):
            if value > cur_max:
                cur_max = value
                index_max = idx
        # add value to sum
        sum_top_three += cur_max
        # remove value from list
        del list_calories[index_max]
    print("Maximum calories of the top three elfs: ", sum_top_three)
