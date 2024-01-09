import numpy as np

HUMAN = 'X'
AI = 'O'
SCORES = {
    HUMAN: -1,
    AI: 1,
    'tie': 0
}


def get_input(user: str, game_map: np.array):
    if user == HUMAN:
        while True:
            print_map(game_map)

            play = int(input(f"Player {user} please make your move (1-9): ")) - 1
            if play < 0 or play >= 9:
                print("Please enter a valid input!")
                continue

            if not game_map[int(play / 3)][play % 3] == " ":
                print("The specified square is not empty!")
                continue

            game_map[int(play / 3)][play % 3] = user
            break
    else:
        ai_move(game_map)


def print_map(game_map: np.array):
    print()
    for i in game_map:
        print("---------------")
        for j in i:
            print(f"| {j} |", end="")
        print()
    print("---------------")


def check_map(game_map: np.array, is_calculation=False) -> str:
    status = None

    for i in range(3):
        if np.all(game_map[i, :] == HUMAN) or np.all(game_map[:, i] == HUMAN):
            status = HUMAN

        elif np.all(game_map[i, :] == AI) or np.all(game_map[:, i] == AI):
            status = AI

    if np.all(np.diag(game_map) == HUMAN) or np.all(np.diag(np.fliplr(game_map)) == HUMAN):
        status = HUMAN

    elif np.all(np.diag(game_map) == AI) or np.all(np.diag(np.fliplr(game_map)) == AI):
        status = AI

    is_tie = True
    for i in game_map:
        for j in i:
            if j == ' ':
                is_tie = False
                break

    if is_tie:
        status = 'tie'

    if status is not None and not is_calculation:
        print_map(game_map)

    return status


def minimax(game_map: np.array, is_maximizing) -> int:
    best_score = -100 if is_maximizing else 100

    result = check_map(game_map, True)
    if result is not None:
        return SCORES.get(result)

    if is_maximizing:  # If it is AI's turn to play then we want to maximize the score
        for i in range(3):
            for j in range(3):
                if game_map[i][j] == ' ':
                    game_map[i][j] = AI
                    score = minimax(game_map, False)
                    game_map[i][j] = ' '

                    best_score = max(score, best_score)

    else:  # If it is HUMAN's turn to play then we want to minimize the score.
        for i in range(3):
            for j in range(3):
                if game_map[i][j] == ' ':
                    game_map[i][j] = HUMAN
                    score = minimax(game_map, True)
                    game_map[i][j] = ' '

                    best_score = min(score, best_score)

    return best_score


def ai_move(game_map) -> None:
    best_move = []
    best_score = -100

    for i in range(3):
        for j in range(3):
            if game_map[i][j] == ' ':
                game_map[i][j] = AI  # Let's assume that AI made this move
                score = minimax(game_map,
                                False)  # Then check what HUMAN ca do to respond this, since this is HUMAN's move we want to minimize it
                game_map[i][j] = ' '  # Then restore the assumed square

                if score > best_score:  # If the calculated score is higher than previous then change it
                    best_score = score
                    best_move = [i, j]

    game_map[best_move[0]][best_move[1]] = AI  # AI makes its move here


def main() -> None:
    game_map = np.full((3, 3), ' ', dtype='str')
    turn = AI

    while check_map(game_map) is None:
        turn = HUMAN if turn == AI else AI
        get_input(turn, game_map)


if __name__ == '__main__':
    main()
