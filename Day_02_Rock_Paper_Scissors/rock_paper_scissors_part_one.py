
__author__ = "Maximilian Geitner"
__date__ = "02.12.2022"


def get_score(first_player, second_player):
    points = 0
    # result matrix
    # A: Rock, B: Paper, C: Scissors
    # X: Rock, Y: Paper, C: Scissors
    # Convert char to ascii value
    first_player_index = ord(first_player) - ord('A')
    second_player_index = ord(second_player) - ord('X')
    # print(first_player_index, second_player_index)
    result_matrix = [[3, 6, 0], [0, 3, 6], [6, 0, 3]]
    # calculate score: points for selected value and result of match
    return second_player_index + 1 + result_matrix[first_player_index][second_player_index]


if __name__ == '__main__':
    file = open('input.txt', 'r')

    score = 0

    for line in file:
        # for each line, evaluate score for given strategy
        # print(line)
        values = line.split(" ")
        val_0 = values[0][0]
        val_1 = values[1][0]
        score += get_score(val_0, val_1)

    print("Total score after all rounds have been completed: ", score)
