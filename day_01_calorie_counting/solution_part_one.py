
__author__ = "Maximilian Geitner"
__date__ = "01.12.2022"


if __name__ == '__main__':
    file = open('input.txt', 'r')
    current_calories = 0
    max_calories = 0
    for line in file:
        # reset counter, if empty line detected
        if line == "\n":
            current_calories = 0
        else:
            # increase current counter and compare with current maximum
            current_calories += int(line)
            if current_calories > max_calories:
                max_calories = current_calories

    file.close()
    print("Maximum calories: ", max_calories)
