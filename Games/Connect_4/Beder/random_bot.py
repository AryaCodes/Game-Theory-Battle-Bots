import random

def random_move(board):
    random_move = random.randint(1, 7)
    if(board.is_valid_move(random_move)):
        return random_move
    else:
        return random_bot()