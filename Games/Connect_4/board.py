import numpy as np

class board:
    """
    Initializing function. Defaults to the standard 6x7 board with 2 players.
    """
    def __init__(self, no_of_players = 2, no_of_rows = 6, no_of_columns = 7, connect_to_win = 4):
        self.__no_of_players = int(no_of_players)
        self.__no_of_columns = int(no_of_columns)
        self.__no_of_rows = int(no_of_rows)
        self.__current_player = 1
        self.__filled_places = 0
        self.__connect_to_win = connect_to_win

        self.__board_state = np.zeros((self.__no_of_rows, self.__no_of_columns))

    """
    Prints the Board in the terminal.
    """
    def print_board(self):
        for row in self.__board_state:
            for element in row:
                if element == 0:
                    element = " "
                if self.__no_of_players == 2:
                    if element == 1:
                        element = "X"
                    elif element == 2:
                        element = "O"
                print(f" |\t{element}\t|", end="")
            print(f"\n")

    """
    return 2D array of game state but with symbols (like X and O) for showing it nicely on front end
    """
    def get_game_as_symbols(self):
        game_as_symbols = self.__board_state
        
        #thanks ChatGPT :)
        if self.__no_of_players == 2:
            game_as_symbols = [
                    [
                        " " if value == 0.0
                        else "X" if value == 1.0 
                        else "O" if value == 2 
                        else value 
                        for value in row
                    ] 
                    for row in game_as_symbols
                ]
            return game_as_symbols
    """
    Returns a copy of the array containing the board state.
    """
    def retrieve_game_state(self):
        return self.__board_state
    
    """
    Returns the current player who's turn it is to move (either 1 or 2)
    """
    def get_current_player(self):
        return self.__current_player

    """
    Returns a boolean on whether the given move is allowed
    """
    def is_valid_move(self, coloumn_number):
        try:
            coloumn_number = int(coloumn_number)
            assert isinstance(coloumn_number, int)
            assert 0<coloumn_number and coloumn_number<self.__no_of_columns+1
        
        except AssertionError as e:
            print("The coloumn number must be a valid positive integer")
            return False
        
        except ValueError as e:
            print("Come on Dope, Atleast enter a number.")
            return False

        __has_space = False
        for x in self.__board_state[:,coloumn_number-1]:
            if x == 0:
                __has_space = True

        if not __has_space:
            print("The coloumn is full choose another one.")
            return False
        
        return True

    """
    Checks and adds a chip to a coloumn if it has space.
    """
    def add_to_coloumn(self, coloumn_number = 1):
        if not self.is_valid_move(coloumn_number):
            return (False, False)
        coloumn_number = int(coloumn_number)
        
        has_won = False
        for y in range(len(self.__board_state[:,coloumn_number-1])):
            x = len(self.__board_state[:,coloumn_number-1]) - y - 1
            if self.__board_state[x,coloumn_number-1] == 0:
                self.__board_state[x,coloumn_number-1] = self.__current_player
                if self.player_has_won(x, coloumn_number-1) == True:
                    has_won = True
                    pass
                else:
                    self.__current_player += 1
                    if self.__current_player> self.__no_of_players:
                        self.__current_player = 1
                break

        self.__filled_places += 1      
        return (True, has_won)

    """Checks all 4 directions to deterime if the played move won the game."""
    def player_has_won(self, row_number, col_number):
        horizontal_to_left = 0
        horizontal_to_right = 0
        vertical_above = 0
        vertical_below = 0
        diagonal_top_left = 0
        diagonal_bottom_right = 0
        diagonal_top_right = 0
        diagonal_bottom_left= 0

        current_player = self.get_current_player()

        x_temp = row_number
        y_temp = col_number

        while True:
            if y_temp == 0: 
                break
            y_temp = y_temp - 1
            if self.__board_state[x_temp, y_temp] == current_player:
                horizontal_to_left += 1
            else: 
                break

        x_temp = row_number
        y_temp = col_number

        while True:
            if y_temp == self.__no_of_columns - 1: 
                break
            y_temp = y_temp + 1
            if self.__board_state[x_temp, y_temp] == current_player:
                horizontal_to_right += 1
            else: 
                break

        x_temp = row_number
        y_temp = col_number

        while True:
            if x_temp == 0: 
                break
            x_temp = x_temp - 1
            if self.__board_state[x_temp, y_temp] == current_player:
                vertical_above += 1
            else: 
                break

        x_temp = row_number
        y_temp = col_number

        while True:
            if x_temp == self.__no_of_rows - 1: 
                break
            x_temp = x_temp + 1
            if self.__board_state[x_temp, y_temp] == current_player:
                vertical_below += 1
            else: 
                break

        x_temp = row_number
        y_temp = col_number

        while True:
            if x_temp == 0 or y_temp==0: 
                break
            x_temp = x_temp - 1
            y_temp = y_temp - 1
            if self.__board_state[x_temp, y_temp] == current_player:
                diagonal_top_left += 1
            else: 
                break

        x_temp = row_number
        y_temp = col_number

        while True:
            if x_temp == 0 or y_temp==self.__no_of_columns-1: 
                break
            x_temp = x_temp - 1
            y_temp = y_temp + 1
            if self.__board_state[x_temp, y_temp] == current_player:
                diagonal_top_right += 1
            else: 
                break

        x_temp = row_number
        y_temp = col_number
        
        while True:
            if x_temp == self.__no_of_rows-1 or y_temp==self.__no_of_columns-1: 
                break
            x_temp = x_temp + 1
            y_temp = y_temp + 1
            if self.__board_state[x_temp, y_temp] == current_player:
                diagonal_bottom_right += 1
            else: 
                break

        x_temp = row_number
        y_temp = col_number
        
        while True:
            if x_temp == self.__no_of_rows-1 or y_temp==0: 
                break
            x_temp = x_temp + 1
            y_temp = y_temp - 1
            if self.__board_state[x_temp, y_temp] == current_player:
                diagonal_bottom_left += 1
            else: 
                break
        
        a = horizontal_to_left + horizontal_to_right + 1
        b = vertical_above + vertical_below + 1
        c = diagonal_top_left + diagonal_bottom_right + 1
        d = diagonal_top_right + diagonal_bottom_left + 1

        if max(a,b,c,d)>= self.__connect_to_win:
            return True

        return False
    
    """
    Returns the current player whose turn it is.
    """
    def get_current_player(self):
        return self.__current_player
    
    """
    Returns true if the whole board is full.
    """
    def is_board_full(self):
        if self.__filled_places >= (self.__no_of_columns*self.__no_of_rows):
            return True
        return False
    
    """
    resets the board to be empty again, but with the same parameters
    """
    def reset_board(self):
        self.__board_state = np.zeros((self.__no_of_rows, self.__no_of_columns))

    """
    let's you load a different board state
    WARNING: This will cause problems if you upload a board state that has a different number of rows and columns
    """
    def load_board(self,  new_board_state, player):
        self.__board_state = new_board_state
        self.__current_player = player