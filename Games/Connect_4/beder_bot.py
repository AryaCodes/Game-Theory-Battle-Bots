import copy
import numpy as np
import board

#TODO FIXES AND IDEAS:
"""
- Getting 3 in a row is dumb because it can immediately be blocked, and with a minimax tree, it should be able to anticipate that
  HOWEVER!! What if the minimax tree ends on me taking a turn? then I won't know the consqequences.
  THEREFORE, minimax tree should always look an even number of turns ahead (mine, yours, mine, yours == 4), so that we can always
  recognize how the opponent will diminish our return value

- incorporate an extra bonus for multi-axis potential score

- backward induction full game tree for when number_of_spaces_left is less than a certain amount

- Orthogonality: does a current eval state of your board clash with potential score in overcounting?
"""
class beder_bot:
    def __init__(self, game_state):
        self.__board_state = game_state
        self.__no_of_rows = len(self.__board_state[:, 0])
        self.__no_of_columns = len(self.__board_state[0])
        self.__connectivity_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns), dtype=object)
        self.__potential_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns), dtype=object)
        self.__score_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns), dtype=object)

    def get_next_move(self, game_state, current_player):
        self.reset_matrices()
        self.__board_state = game_state
        self.initialize_score_arrays(current_player)

        all_possible_moves = self.get_all_possible_moves()
        return self.pick_best_move(all_possible_moves)

    #TODO replacing places that already have a piece with 0 isn't the wisest thing
    def initialize_score_arrays(self, current_player):
        opposite_player = self.get_opposite_player(current_player)
        for row_num in range(self.__no_of_rows):
            for col_num in range(self.__no_of_columns):
                if self.__board_state[row_num, col_num] != current_player:
                    score = self.evaluate_piece(row_num, col_num, current_player)
                    connectivity_value = score[0]
                    potential_value = score[1]
                    self.__connectivity_matrix[row_num, col_num] = connectivity_value
                    self.__potential_matrix[row_num, col_num] = potential_value
                    self.__score_matrix[row_num, col_num] = connectivity_value + potential_value
                elif self.__board_state[row_num, col_num] == opposite_player:
                    opposite_player_symbol = self.get_piece_symbol(opposite_player)
                    self.__connectivity_matrix[row_num, col_num] = opposite_player_symbol
                    self.__potential_matrix[row_num, col_num] = opposite_player_symbol
                    self.__score_matrix[row_num, col_num] = opposite_player_symbol
                else:
                    self.__connectivity_matrix[row_num, col_num] = " "
                    self.__potential_matrix[row_num, col_num] = " "
                    self.__score_matrix[row_num, col_num] = " "
                
                # if self.__board_state[row_num, col_num] != 0:
                #     self.__connectivity_matrix[row_num, col_num] = 0
                #     self.__potential_matrix[row_num, col_num] = 0
                #     self.__score_matrix[row_num, col_num] = 0
                # else:
                #     score = self.calculate_score(row_num, col_num, current_player)
                #     connectivity_value = score[0]
                #     potential_value = score[1]
                #     self.__connectivity_matrix[row_num, col_num] = connectivity_value
                #     self.__potential_matrix[row_num, col_num] = potential_value
                #     self.__score_matrix[row_num, col_num] = connectivity_value + potential_value

    def evaluate_piece(self, row_num, col_num, current_player):
        horizontal_to_left = 0
        horizontal_to_right = 0
        vertical_above = 0
        vertical_below = 0
        diagonal_top_left = 0
        diagonal_bottom_right = 0
        diagonal_top_right = 0
        diagonal_bottom_left= 0

        same_left = 0
        same_right = 0
        same_above = 0
        same_below = 0
        same_top_left = 0
        same_bottom_right = 0
        same_top_right = 0
        same_bottom_left = 0

        is_left_open = True
        is_right_open = True
        is_above_open = True
        is_below_open = True
        is_top_left_open = True
        is_bottom_right_open = True
        is_top_right_open = True
        is_bottom_left_open = True

        x_temp = row_num
        y_temp = col_num

        opposite_player = self.get_opposite_player(current_player)

        while True:
            if y_temp == 0 or horizontal_to_left >= 3: 
                break
            y_temp = y_temp - 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                is_left_open = False
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_left += 1
            horizontal_to_left += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if y_temp == self.__no_of_columns - 1 or horizontal_to_right >= 3: 
                break
            y_temp = y_temp + 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                is_right_open = False
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_right += 1
            horizontal_to_right += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == 0  or vertical_above >= 3: 
                break
            x_temp = x_temp - 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                is_above_open = False
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_above += 1
            vertical_above += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == self.__no_of_rows - 1  or vertical_below >= 3: 
                break
            x_temp = x_temp + 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                is_below_open = False
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_below += 1
            vertical_below += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == 0 or y_temp==0 or diagonal_top_left >= 3: 
                break
            x_temp = x_temp - 1
            y_temp = y_temp - 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                is_top_left_open = False
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_top_left += 1
            diagonal_top_left += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == 0 or y_temp==self.__no_of_columns-1 or diagonal_top_right >= 3: 
                break
            x_temp = x_temp - 1
            y_temp = y_temp + 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                is_top_right_open = False
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_top_right += 1
            diagonal_top_right += 1

        x_temp = row_num
        y_temp = col_num
        
        while True:
            if x_temp == self.__no_of_rows-1 or y_temp==self.__no_of_columns-1 or diagonal_bottom_right >= 3: 
                break
            x_temp = x_temp + 1
            y_temp = y_temp + 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                is_bottom_right_open = False
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_bottom_right+= 1
            diagonal_bottom_right += 1

        x_temp = row_num
        y_temp = col_num
        
        while True:
            if x_temp == self.__no_of_rows-1 or y_temp==0 or diagonal_bottom_left >= 3: 
                break
            x_temp = x_temp + 1
            y_temp = y_temp - 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                is_bottom_left_open = False
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_bottom_left += 1
            diagonal_bottom_left += 1
        
        horizontal_connectivity = self.num_of_possible_wins(horizontal_to_left + horizontal_to_right + 1)
        vertical_connectivity = self.num_of_possible_wins(vertical_above + vertical_below + 1)
        neg_diagonal_connectivity = self.num_of_possible_wins(diagonal_top_left + diagonal_bottom_right + 1)
        pos_diagonal_connectivity = self.num_of_possible_wins(diagonal_top_right + diagonal_bottom_left + 1)

        horizontal_potential = self.potential_score(same_left + same_right + 1, is_left_open + is_right_open)
        vertical_potential = self.potential_score(same_above + same_below + 1, is_above_open + is_below_open)
        neg_diagonal_potential = self.potential_score(same_top_left + same_bottom_right + 1, is_top_left_open + is_bottom_right_open)
        pos_diagonal_potential = self.potential_score(same_top_right + same_bottom_left + 1, is_top_right_open + is_bottom_left_open)

        connectivity = horizontal_connectivity + vertical_connectivity + neg_diagonal_connectivity + pos_diagonal_connectivity
        potential = horizontal_potential + vertical_potential + neg_diagonal_potential + pos_diagonal_potential
        return (connectivity, potential)

    #TODO how do I include blocking opponent? is that covered in minmax when the opponent is calculated?
    def calculate_score(self, row_num, col_num, current_player):
        horizontal_to_left = 0
        horizontal_to_right = 0
        vertical_above = 0
        vertical_below = 0
        diagonal_top_left = 0
        diagonal_bottom_right = 0
        diagonal_top_right = 0
        diagonal_bottom_left= 0

        same_left = 0
        same_right = 0
        same_above = 0
        same_below = 0
        same_top_left = 0
        same_bottom_right = 0
        same_top_right = 0
        same_bottom_left = 0

        x_temp = row_num
        y_temp = col_num

        opposite_player = self.get_opposite_player(current_player)

        while True:
            if y_temp == 0 or horizontal_to_left >= 3: 
                break
            y_temp = y_temp - 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_left += 1
            horizontal_to_left += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if y_temp == self.__no_of_columns - 1 or horizontal_to_right >= 3: 
                break
            y_temp = y_temp + 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_right += 1
            horizontal_to_right += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == 0  or vertical_above >= 3: 
                break
            x_temp = x_temp - 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_above += 1
            vertical_above += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == self.__no_of_rows - 1  or vertical_below >= 3: 
                break
            x_temp = x_temp + 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_below += 1
            vertical_below += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == 0 or y_temp==0 or diagonal_top_left >= 3: 
                break
            x_temp = x_temp - 1
            y_temp = y_temp - 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_top_left += 1
            diagonal_top_left += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == 0 or y_temp==self.__no_of_columns-1 or diagonal_top_right >= 3: 
                break
            x_temp = x_temp - 1
            y_temp = y_temp + 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_top_right += 1
            diagonal_top_right += 1

        x_temp = row_num
        y_temp = col_num
        
        while True:
            if x_temp == self.__no_of_rows-1 or y_temp==self.__no_of_columns-1 or diagonal_bottom_right >= 3: 
                break
            x_temp = x_temp + 1
            y_temp = y_temp + 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_bottom_right+= 1
            diagonal_bottom_right += 1

        x_temp = row_num
        y_temp = col_num
        
        while True:
            if x_temp == self.__no_of_rows-1 or y_temp==0 or diagonal_bottom_left >= 3: 
                break
            x_temp = x_temp + 1
            y_temp = y_temp - 1
            if self.__board_state[x_temp, y_temp] == opposite_player:
                break
            if self.__board_state[x_temp, y_temp] == current_player:
                same_bottom_left += 1
            diagonal_bottom_left += 1
        
        horizontal_connectivity = self.num_of_possible_wins(horizontal_to_left + horizontal_to_right + 1)
        vertical_connectivity = self.num_of_possible_wins(vertical_above + vertical_below + 1)
        neg_diagonal_connectivity = self.num_of_possible_wins(diagonal_top_left + diagonal_bottom_right + 1)
        pos_diagonal_connectivity = self.num_of_possible_wins(diagonal_top_right + diagonal_bottom_left + 1)

        horizontal_potential = self.potential_score(same_left + same_right)
        vertical_potential = self.potential_score(same_above + same_below)
        neg_diagonal_potential = self.potential_score(same_top_left + same_bottom_right)
        pos_diagonal_potential = self.potential_score(same_top_right + same_bottom_left)

        connectivity = horizontal_connectivity + vertical_connectivity + neg_diagonal_connectivity + pos_diagonal_connectivity
        potential = horizontal_potential + vertical_potential + neg_diagonal_potential + pos_diagonal_potential
        return (connectivity, potential)

    def num_of_possible_wins(self, num_of_adjacent_spaces):
        if num_of_adjacent_spaces == 4:
            return 1
        elif num_of_adjacent_spaces == 5:
            return 2
        elif num_of_adjacent_spaces == 6:
            return 3
        elif num_of_adjacent_spaces == 7:
            return 4
        else:
            return 0
        
    def potential_score(self, num_of_adjacent_pieces_in_a_row, how_many_directions_open):
        if num_of_adjacent_pieces_in_a_row == 1:
            return 0
        return 2**num_of_adjacent_pieces_in_a_row * how_many_directions_open

    #TODO Break ties later
    def pick_best_move(self, possible_moves):
        highest_score = 0
        best_col = -1
        for move in possible_moves:
            move_row = move[0]
            move_col = move[1]
            move_score = self.__score_matrix[move_row][move_col]
            if move_score >= highest_score:
                highest_score = move_score
                best_col = move_col
        
        return best_col + 1

    def get_all_possible_moves(self):
        all_possible_moves = []
        for col_num in range(self.__no_of_columns):
            move = self.where_does_input_land(col_num)
            if move != (-1, -1):
                all_possible_moves.append(move)

        return all_possible_moves
    
    def where_does_input_land(self, col_num):
        col_num += 1
        for y in range(len(self.__board_state[:,col_num-1])):
            x = len(self.__board_state[:,col_num-1]) - y - 1
            if self.__board_state[x][col_num-1] == 0:
                return (x,col_num-1)
        
        return (-1,-1)
    
    def get_all_piece_positions(self, player):
        player_piece_positions = []
        for row_num in range(self.__no_of_rows):
            for col_num in range(self.__no_of_columns):
                if self.__board_state[row_num][col_num] == player:
                    player_piece_positions.append((row_num, col_num))
        
        return player_piece_positions

    def print_connectivity_matrix(self):
        print("connectivity matrix:")
        for row in self.__connectivity_matrix:
            for element in row:
                print(f" |\t{element}\t|", end="")
            print(f"\n")

    def print_potential_matrix(self):
        print("potential matrix:")
        for row in self.__potential_matrix:
            for element in row:
                print(f" |\t{element}\t|", end="")
            print(f"\n")

    def print_score_matrix(self):
        print("score matrix:")
        for row in self.__score_matrix:
            for element in row:
                print(f" |\t{element}\t|", end="")
            print(f"\n")

    def get_opposite_player(self, turn):
        if turn == 1:
            return 2
        elif turn == 2:
            return 1
        
    def get_piece_symbol(self, player):
        if player == 1:
            return "X"
        elif player == 2:
            return "Y"
        
    def reset_matrices(self):
        self.__connectivity_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns))
        self.__potential_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns))
        self.__score_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns))


# if __name__ == "__main__":
#     num_play =  2
#     num_rows = 6
#     num_col = 7
#     num_connect = 4
#     test_board = board.board(num_play, num_rows, num_col, num_connect)
#     bot = beder_bot(test_board)
#     test_board.print_board()
    
#     print("init")
#     move = bot.get_next_move(test_board.retrieve_game_state(), 1)
#     bot.print_connectivity_matrix()
#     bot.print_potential_matrix()
#     bot.print_score_matrix()
#     test_board.add_to_coloumn(move)
#     print("----------------------------------")
#     test_board.print_board()
    
#     move = bot.get_next_move(test_board.retrieve_game_state(), 2)
#     bot.print_connectivity_matrix()
#     bot.print_potential_matrix()
#     bot.print_score_matrix()
#     print("first move done")
#     test_board.add_to_coloumn(move)
#     print("----------------------------------")
#     test_board.print_board()
    
#     move = bot.get_next_move(test_board.retrieve_game_state(), 1)
#     bot.print_connectivity_matrix()
#     bot.print_potential_matrix()
#     bot.print_score_matrix()
#     print("second move done")