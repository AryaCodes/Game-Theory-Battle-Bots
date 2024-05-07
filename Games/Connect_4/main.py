import board
from beder_bot import beder_bot
import copy

if __name__ == "__main__":
    num_play =  2
    num_rows = 6
    num_col = 7
    num_connect = 4
    test = board.board(num_play, num_rows, num_col, num_connect)

    game_won = False
    bot = beder_bot(test.retrieve_game_state())
    while True:
        test.print_board()
        bot_move = bot.get_next_move(copy.copy(test.retrieve_game_state()), test.get_current_player())
        # bot.print_connectivity_matrix()
        # bot.print_potential_matrix()
        bot.print_score_matrix()
        print(f"Player {test.get_current_player()}s Turn. Enter a coloumn to play chip-'")
        # col_no = input()
        col_no = bot_move
        # col_no = random_bot(test.retrieve_game_state(), test.get_current_player())
        Add = test.add_to_coloumn(col_no)
        if Add[0] == False:
            print("Try again.")
        elif Add[1] == True:
            print(f"Player {test.get_current_player()} has won. Congratulations!'")
            test.print_board()
            break
        elif test.is_board_full():
            print("No more moves can be played. Big Sad. It's a tie.")
            test.print_board()
            break
        
    pass

