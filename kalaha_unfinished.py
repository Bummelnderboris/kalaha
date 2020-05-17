P1 = "Player 1"  # player1
P2 = "Player 2"  # player2


def isGameOver(game):
    p1_side_empty = all(pos == 0 for pos in game.board[:5])
    p2_side_empty = all(pos == 0 for pos in game.board[6:])
    return p1_side_empty or p2_side_empty


def print_game(game):
    board = game.board
    p1_score = game.P1_score
    p2_score = game.P2_score
    print("\n")
    print(f"P1: \t{list(reversed(board[:6]))}\t P2:")   #suggestion from friend (I don't understand the exaxt advantage of f bracket)
    print(f"{p1_score} \t{board[6:]}\t {p2_score}")     #suggestion from friend (I don't understand the exaxt advantage of f bracket)
    print("\n")


def distribute(game_original, move_pos):
    game = game_original
    in_hand = game.board[move_pos]
    game.board[move_pos] = 0
    i = move_pos + 1
    while in_hand > 0:
        # If the turn ends on an empty pocket
        try:
            if game.board[i] == 0 and in_hand == 1:
                if game.turn == P1:
                    if i < 6:
                        game.P1_score += 1 + game.board[i+6]
                        in_hand = 0
                        game.board[i+6] = 0
                    else:
                        game.P1_score += 1
                        in_hand = 0
                elif game.turn == P2:
                    if i < 6:
                        game.P2_score += 1
                        in_hand = 0
                    else:
                        game.P2_score += 1 + game.board[i-6]
                        in_hand = 0
                        game.board[i-6] = 0
                continue
        except Exception:
            # print(game.board)
            # print(i)
            pass
            
        # If the turn is a P1 Kalaha
        if i == 6 and game.turn == P1:
            game.P1_score += 1
            in_hand -= 1
            if in_hand == 0:
                print("\n🏄 Kalaha - play again")
                print_game(game)
                return make_move(game)
        # else if the turn is a P2 Kalaha
        elif i == 12:
            if game.turn == P2:
                game.P2_score += 1
                in_hand -= 1
                if in_hand == 0:
                    print("\n🏄 Kalaha - play again")
                    print_game(game)
                    return make_move(game)
            i = 0
        game.board[i] += 1
        in_hand -= 1
        i += 1
    return game


def make_move(game):
    move_pos = get_input(game.turn)
    return distribute(game, move_pos)


def error_message(ip, message):
    print(f"{ip} is not valid.")
    print(message)


def get_input(turn):
    message = "P1 input: " if turn == P1 else "P2 input: "
    range_start, range_end = (0, 5) if turn == P1 else (6, 11)
    pos = 0
    user_ip = input(message)
    try:
        pos = int(user_ip)
    except ValueError:
        error_message(user_ip, "Please input a number!\n")
        return get_input(turn)
    if pos < range_start or pos > range_end:
        error_message(user_ip, f"Range: {range_start} and {range_end}")
        return get_input(turn)
    return pos


def kalaha(game):
    if isGameOver(game):
        return get_winner(game)
    else:
        next_game = make_move(game)
        next_game.turn = P2 if game.turn is P1 else P1
        print_game(next_game)
        return kalaha(next_game)


def get_winner(game):
    if game.P1_score > game.P2_score:
        return P1
    elif game.P1_score < game.P2_score:
        return P2
    else:
        return None


class Game:
    def __init__(self, turn):
        self.board = [4] * 12
        self.P1_score = 0
        self.P2_score = 0
        self.turn = turn


def print_winner(winner):
    if not winner:
        print("It is a draw!")
    else:
        print("The winner is " + winner)


def new_game():
    return Game(P1)


if __name__ == "__main__":
    empty_game = new_game()
    print_game(empty_game)
    winner = kalaha(empty_game)
    print_winner(winner)
