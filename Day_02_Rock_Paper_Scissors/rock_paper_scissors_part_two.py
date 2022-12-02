
__author__ = "Maximilian Geitner"
__date__ = "02.12.2022"


def get_score(first_player, second_player):
    points = 0
    # result matrix
    # A: Rock, B: Paper, C: Scissors
    # X: Loss, Y: Draw, Z: Win
    # Convert char to ascii value
    first_player_index = ord(first_player) - ord('A')
    second_player_index = ord(second_player) - ord('X')
    # matrix with mapping (player_one, match_result) => points for choice (rock, paper, scissors)
    result_selected_value = [[3, 1, 2], [1, 2, 3], [2, 3, 1]]
    # 0 points for loss, 3 points for draw, 6 points for win
    result_match = [0, 3, 6]
    # calculate score: points for result of match and selected value
    return result_match[second_player_index] + result_selected_value[first_player_index][second_player_index]


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
