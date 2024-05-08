import numpy as np
import copy

#TODO FIXES AND IDEAS:
"""
- backward induction full game tree for when number_of_spaces_left is less than a certain amount
"""
class beder_bot:
    def __init__(self, board):
        self.__board = board
        self.__board_state = board.retrieve_game_state()
        self.__no_of_rows = len(self.__board_state[:, 0])
        self.__no_of_columns = len(self.__board_state[0])
        self.__connectivity_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns), dtype=object)
        self.__potential_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns), dtype=object)
        self.__score_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns), dtype=object)
        self.__opponent_score_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns), dtype=object)

    def get_next_move(self, game_state, current_player):
        self.reset_matrices()
        self.__board.load_board(copy.copy(game_state), current_player)
        self.__board_state = copy.copy(game_state)

        self.initialize_score_arrays(current_player)

        how_many_spaces_left = self.how_many_spaces_left(game_state)
        how_many_columns_left = len(self.get_all_possible_moves(game_state))
        if how_many_spaces_left <= 8:
            best_move = self.pick_best_move(how_many_spaces_left, current_player)    
            return best_move

        if how_many_columns_left <= 4 and how_many_spaces_left <= 12:
            best_move = self.pick_best_move(how_many_spaces_left, current_player)    
            return best_move

        best_move = self.pick_best_move(4, current_player)
        return best_move

    def pick_best_move(self, depth, current_player):
        all_possible_moves = self.get_all_possible_moves(self.__board_state)
        best_score = float('-inf')
        best_col_move = None

        opposite_player = self.get_opposite_player(current_player)
        for move in all_possible_moves:
            temp_board = copy.copy(self.__board)
            temp_board.load_board(copy.copy(self.__board_state), copy.copy(current_player))
            temp_score_matrix = copy.copy(self.__score_matrix)
            temp_opponent_score_matrix = copy.copy(self.__opponent_score_matrix)
            
            score = self.minimax(move, depth - 1, current_player, False, temp_board, temp_opponent_score_matrix, temp_score_matrix, opposite_player)
            if score > best_score:
                best_score = score
                best_col_move = move[1]
        
        return best_col_move

    #TODO Add earlier depth preference
    """
    - connectivity amplification?
    - top ceiling as a blocker to axis
    """
    def minimax(self, move, depth, original_player, is_maxing, board, score_matrix, opponent_score_matrix, current_player):
        opposite_player = self.get_opposite_player(original_player)
        if board.player_has_won(move[0], move[1]) and current_player==original_player:
            return -1000
        elif board.player_has_won(move[0], move[1]) and current_player==opposite_player:
            return 1000

        next_player = self.get_opposite_player(current_player)
        board.add_to_coloumn(move[1] + 1) #TODO could be source for mistake later
        new_game_state = board.retrieve_game_state()
        self.update_evaluations(move[0], move[1], new_game_state, score_matrix, opponent_score_matrix, next_player) #next == previous that did move
        if self.is_board_full(new_game_state):
            return 0
        elif depth == 0:
            self_eval = self.get_evaluation(score_matrix)
            opponent_eval = self.get_evaluation(opponent_score_matrix)
            return self_eval - opponent_eval

        if is_maxing:
            best_score = float('-inf')
            all_possible_moves = self.get_all_possible_moves(new_game_state)
            for new_move in all_possible_moves:
                temp_board = copy.copy(board)
                temp_board.load_board(copy.copy(new_game_state), copy.copy(current_player))
                temp_score_matrix = copy.copy(score_matrix)
                temp_opponent_score_matrix = copy.copy(opponent_score_matrix)
                score = self.minimax(new_move, depth - 1, original_player, False, temp_board, temp_opponent_score_matrix, temp_score_matrix, next_player)
                best_score = max(score, best_score)
            return best_score
        else:
            min_score = float('inf')
            all_possible_moves = self.get_all_possible_moves(new_game_state)
            for new_move in all_possible_moves:
                temp_board = copy.copy(board)
                temp_board.load_board(copy.copy(new_game_state), copy.copy(current_player))
                temp_score_matrix = copy.copy(score_matrix)
                temp_opponent_score_matrix = copy.copy(opponent_score_matrix)
                score = self.minimax(new_move, depth - 1, original_player, True, temp_board, temp_opponent_score_matrix, temp_score_matrix, next_player)
                min_score = min(score, min_score)
            return min_score

    def update_evaluations(self, row_num, col_num, game_state, score_matrix, opponent_score_matrix, player_that_made_move):
        opposite_player = self.get_opposite_player(player_that_made_move)
        
        score = self.evaluate_piece(row_num, col_num, player_that_made_move, game_state)
        updated_value = score[0] + score[1]
        opponent_score_matrix[row_num][col_num] = updated_value
        opponent_symbol = self.get_piece_symbol(player_that_made_move)
        score_matrix[row_num][col_num] = opponent_symbol

        
        pieces_that_need_evaluation = self.get_pieces_that_need_reevluation_per_player(row_num, col_num, game_state, opposite_player)
        for piece in pieces_that_need_evaluation:
            score = self.evaluate_piece(piece[0], piece[1], opposite_player, game_state)
            updated_value = score[0] + score[1]
            score_matrix[piece[0]][piece[1]] = updated_value

        #evaluate opponent pieces (comment deprecated??)
        pieces_that_need_evaluation = self.get_pieces_that_need_reevluation_per_player(row_num, col_num, game_state, player_that_made_move)
        for piece in pieces_that_need_evaluation:
            score = self.evaluate_piece(piece[0], piece[1], player_that_made_move, game_state)
            updated_value = score[0] + score[1]
            opponent_score_matrix[piece[0]][piece[1]] = updated_value

    def get_pieces_that_need_reevluation_per_player(self, row_num, col_num, game_state, player_to_check):
        pieces_that_need_reevaluation = []
        
        horizontal_to_left = 0
        horizontal_to_right = 0
        vertical_above = 0
        vertical_below = 0
        diagonal_top_left = 0
        diagonal_bottom_right = 0
        diagonal_top_right = 0
        diagonal_bottom_left= 0

        x_temp = row_num
        y_temp = col_num

        opposite_player = self.get_opposite_player(player_to_check)

        while True:
            if y_temp == 0 or horizontal_to_left >= 3: 
                break
            y_temp = y_temp - 1
            if game_state[x_temp, y_temp] == opposite_player:
                break
            if game_state[x_temp, y_temp] == player_to_check:
                pieces_that_need_reevaluation.append((x_temp, y_temp))
            horizontal_to_left += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if y_temp == self.__no_of_columns - 1 or horizontal_to_right >= 3: 
                break
            y_temp = y_temp + 1
            if game_state[x_temp, y_temp] == opposite_player:
                break
            if game_state[x_temp, y_temp] == player_to_check:
                pieces_that_need_reevaluation.append((x_temp, y_temp))
            horizontal_to_right += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == 0  or vertical_above >= 3: 
                break
            x_temp = x_temp - 1
            if game_state[x_temp, y_temp] == opposite_player:
                break
            if game_state[x_temp, y_temp] == player_to_check:
                pieces_that_need_reevaluation.append((x_temp, y_temp))
            vertical_above += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == self.__no_of_rows - 1  or vertical_below >= 3: 
                break
            x_temp = x_temp + 1
            if game_state[x_temp, y_temp] == opposite_player:
                break
            if game_state[x_temp, y_temp] == player_to_check:
                pieces_that_need_reevaluation.append((x_temp, y_temp))
            vertical_below += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == 0 or y_temp==0 or diagonal_top_left >= 3: 
                break
            x_temp = x_temp - 1
            y_temp = y_temp - 1
            if game_state[x_temp, y_temp] == opposite_player:
                break
            if game_state[x_temp, y_temp] == player_to_check:
                pieces_that_need_reevaluation.append((x_temp, y_temp))
            diagonal_top_left += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == 0 or y_temp==self.__no_of_columns-1 or diagonal_top_right >= 3: 
                break
            x_temp = x_temp - 1
            y_temp = y_temp + 1
            if game_state[x_temp, y_temp] == opposite_player:
                break
            if game_state[x_temp, y_temp] == player_to_check:
                pieces_that_need_reevaluation.append((x_temp, y_temp))
            diagonal_top_right += 1

        x_temp = row_num
        y_temp = col_num
        
        while True:
            if x_temp == self.__no_of_rows-1 or y_temp==self.__no_of_columns-1 or diagonal_bottom_right >= 3: 
                break
            x_temp = x_temp + 1
            y_temp = y_temp + 1
            if game_state[x_temp, y_temp] == opposite_player:
                break
            if game_state[x_temp, y_temp] == player_to_check:
                pieces_that_need_reevaluation.append((x_temp, y_temp))
            diagonal_bottom_right += 1

        x_temp = row_num
        y_temp = col_num
        
        while True:
            if x_temp == self.__no_of_rows-1 or y_temp==0 or diagonal_bottom_left >= 3: 
                break
            x_temp = x_temp + 1
            y_temp = y_temp - 1
            if game_state[x_temp, y_temp] == opposite_player:
                break
            if game_state[x_temp, y_temp] == player_to_check:
                pieces_that_need_reevaluation.append((x_temp, y_temp))
            diagonal_bottom_left += 1
        
        return pieces_that_need_reevaluation

    def get_evaluation(self, score_matrix):
        total_eval = 0
        for row_num in range(self.__no_of_rows):
            for col_num in range(self.__no_of_columns):
                isInt = isinstance(score_matrix[row_num, col_num], int) #either " " or symbol(x or O) or score for that slot
                isFloat = isinstance(score_matrix[row_num, col_num], float) #either " " or symbol(x or O) or score for that slot
                if isInt or isFloat:
                    value = int(score_matrix[row_num, col_num])
                    total_eval += value
        
        return total_eval

    def initialize_score_arrays(self, current_player):
        opposite_player = self.get_opposite_player(current_player)
        for row_num in range(self.__no_of_rows):
            for col_num in range(self.__no_of_columns):
                if self.__board_state[row_num, col_num] == current_player:
                    score = self.evaluate_piece(row_num, col_num, current_player, self.__board_state)
                    connectivity_value = score[0]
                    potential_value = score[1]
                    self.__connectivity_matrix[row_num, col_num] = connectivity_value
                    self.__potential_matrix[row_num, col_num] = potential_value
                    self.__score_matrix[row_num, col_num] = connectivity_value + potential_value

                    #updating opponent score matrix with symbol
                    current_player_symbol = self.get_piece_symbol(current_player)
                    self.__opponent_score_matrix[row_num, col_num] = current_player_symbol
                elif self.__board_state[row_num, col_num] == opposite_player:
                    score = self.evaluate_piece(row_num, col_num, opposite_player, self.__board_state)
                    connectivity_value = score[0]
                    potential_value = score[1]
                    self.__opponent_score_matrix[row_num, col_num] = connectivity_value + potential_value

                    #updating this player's matrices with opponent's symbol
                    opposite_player_symbol = self.get_piece_symbol(opposite_player)
                    self.__connectivity_matrix[row_num, col_num] = opposite_player_symbol
                    self.__potential_matrix[row_num, col_num] = opposite_player_symbol
                    self.__score_matrix[row_num, col_num] = opposite_player_symbol
                else:
                    self.__connectivity_matrix[row_num, col_num] = " "
                    self.__potential_matrix[row_num, col_num] = " "
                    self.__score_matrix[row_num, col_num] = " "
                    self.__opponent_score_matrix[row_num, col_num] = " "

    def evaluate_piece(self, row_num, col_num, current_player, game_state):
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
            if y_temp == 0:
                is_left_open = False
                break
            elif horizontal_to_left >= 3: 
                break
            y_temp = y_temp - 1
            if game_state[x_temp, y_temp] == opposite_player:
                is_left_open = False
                break
            if game_state[x_temp, y_temp] == current_player:
                same_left += 1
            horizontal_to_left += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if y_temp == self.__no_of_columns - 1:
                is_right_open = False
                break
            elif horizontal_to_right >= 3: 
                break
            y_temp = y_temp + 1
            if game_state[x_temp, y_temp] == opposite_player:
                is_right_open = False
                break
            if game_state[x_temp, y_temp] == current_player:
                same_right += 1
            horizontal_to_right += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == self.__no_of_rows - 1:
                is_above_open = False
                break
            elif vertical_above >= 3:
                break
            x_temp = x_temp + 1
            if game_state[x_temp, y_temp] == opposite_player:
                is_above_open = False
                break
            if game_state[x_temp, y_temp] == current_player:
                same_above += 1
            vertical_above += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == 0:
                is_below_open = False
                break
            elif vertical_below >= 3: 
                break
            x_temp = x_temp - 1
            if game_state[x_temp, y_temp] == opposite_player:
                is_below_open = False
                break
            if game_state[x_temp, y_temp] == current_player:
                same_below += 1
            vertical_below += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == 0 or y_temp==0:
                is_top_left_open = False
                break
            elif diagonal_top_left >= 3:
                break
            x_temp = x_temp - 1
            y_temp = y_temp - 1
            if game_state[x_temp, y_temp] == opposite_player:
                is_top_left_open = False
                break
            if game_state[x_temp, y_temp] == current_player:
                same_top_left += 1
            diagonal_top_left += 1

        x_temp = row_num
        y_temp = col_num

        while True:
            if x_temp == 0 or y_temp==self.__no_of_columns-1:
                is_top_right_open = False
                break
            elif diagonal_top_right >= 3: 
                break
            x_temp = x_temp - 1
            y_temp = y_temp + 1
            if game_state[x_temp, y_temp] == opposite_player:
                is_top_right_open = False
                break
            if game_state[x_temp, y_temp] == current_player:
                same_top_right += 1
            diagonal_top_right += 1

        x_temp = row_num
        y_temp = col_num
        
        while True:
            if x_temp == self.__no_of_rows-1 or y_temp==self.__no_of_columns-1:
                is_bottom_right_open = False
                break
            elif diagonal_bottom_right >= 3:
                break
            x_temp = x_temp + 1
            y_temp = y_temp + 1
            if game_state[x_temp, y_temp] == opposite_player:
                is_bottom_right_open = False
                break
            if game_state[x_temp, y_temp] == current_player:
                same_bottom_right+= 1
            diagonal_bottom_right += 1

        x_temp = row_num
        y_temp = col_num
        
        while True:
            if x_temp == self.__no_of_rows-1 or y_temp==0:
                is_bottom_left_open = False
                break
            elif diagonal_bottom_left >= 3: 
                break
            x_temp = x_temp + 1
            y_temp = y_temp - 1
            if game_state[x_temp, y_temp] == opposite_player:
                is_bottom_left_open = False
                break
            if game_state[x_temp, y_temp] == current_player:
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
        
    def potential_score(self, num_pieces_in_a_row, how_many_directions_open):
        if num_pieces_in_a_row == 1:
            return 0

        #divided by num_pieces_in_a_row so that if the total score for a pattern is X, then each piece of that pattern will have a portion of that score
        return (2**num_pieces_in_a_row * how_many_directions_open) / num_pieces_in_a_row

    #Returns col between 0 - 6
    def get_all_possible_moves(self, game_state):
        all_possible_moves = []
        for col_num in range(self.__no_of_columns):
            move = self.where_does_input_land(col_num, game_state)
            if move != (-1, -1):
                all_possible_moves.append(move)

        return all_possible_moves
    
    #Returns col between 0 - 6
    def where_does_input_land(self, col_num, game_state):
        col_num += 1
        for y in range(len(game_state[:,col_num-1])):
            x = len(game_state[:,col_num-1]) - y - 1
            if game_state[x][col_num-1] == 0:
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

    def get_opposite_player(self, current_player):
        if current_player == 1:
            return 2
        elif current_player == 2:
            return 1
        
    def get_piece_symbol(self, player):
        if player == 1:
            return "X"
        elif player == 2:
            return "O"
        
    def reset_matrices(self):
        self.__connectivity_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns), dtype=object)
        self.__potential_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns), dtype=object)
        self.__score_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns), dtype=object)
        self.__opponent_score_matrix = np.zeros((self.__no_of_rows, self.__no_of_columns), dtype=object)
    
    def is_board_full(self, game_state):
        filled_places = 0
        for row_num in range(self.__no_of_rows):
            for col_num in range(self.__no_of_columns):
                if game_state[row_num][col_num] == 0:
                    filled_places += 1

        if filled_places >= (self.__no_of_columns*self.__no_of_rows):
            return True
        return False

    def how_many_spaces_left(self, game_state):
        filled_places = 0
        for row_num in range(self.__no_of_rows):
            for col_num in range(self.__no_of_columns):
                if game_state[row_num][col_num] == 0:
                    filled_places += 1

        return filled_places