import board

if __name__ == "__main__":
    num_play =  2
    num_rows = 6
    num_col = 7
    num_connect = 4
    test = board.board(num_play, num_rows, num_col, num_connect)

    game_won = False
    while True:
        test.print_board()
        print(f"Player {test.get_current_player()}s Turn. Enter a coloumn to play chip-'")
        col_no = input()
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

