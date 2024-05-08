import numpy as np

class Arya_Bot:

    def __init__(self):
        pass

    def play_move(self, game_state, current_player, filled_places, depth = 0):
        self.game_state = game_state 
        self.current_player = current_player
        self.opponet_player = self.set_opponent_player()
        (self.no_of_rows, self.no_of_coloumns) = game_state.shape
        self.depth = depth
        self.filled_places = filled_places

        self.current_player_value = [-0.001 for _ in range(self.no_of_coloumns)]
        self.current_player_row = ['x' for _ in range(self.no_of_coloumns)]
        self.opponent_player_value = [-0.001 for _ in range(self.no_of_coloumns)]
        self.total_player_value = [-0.001 for _ in range(self.no_of_coloumns)]
        self.col_is_full = [True for _ in range(self.no_of_coloumns)]

        depth_check = 4

        if self.depth == 4:
            return (0,-0.001)

        #This checks which coloumns actually have space.
        for col_no in range(self.no_of_coloumns):
            for x in range(len(self.game_state[:,col_no])):
                if self.game_state[x,col_no] == 0:
                    self.current_player_value[col_no] = 'o'
                    self.current_player_row[col_no] = x
                    self.col_is_full[col_no] = False

        for col_no in range(self.no_of_coloumns):
            if self.current_player_value[col_no] == 'o':
                self.current_player_value[col_no] = self.calculate_current_player_value(self.current_player_row[col_no], col_no)
          
        #print(self.current_player_value)

        for col_no in range(self.no_of_coloumns):
            temp_game_state = self.game_state.copy()
            mini_bot = Arya_Bot()

            if self.current_player_value[col_no] != -0.001:
                temp_game_state[self.current_player_row[col_no], col_no] = self.current_player
                self.opponent_player_value[col_no] = mini_bot.play_move(temp_game_state, self.opponet_player, self.filled_places, depth + 1)[1]

        #print(self.current_player_value, self.opponent_player_value)
        for col_no in range(self.no_of_coloumns):
            self.total_player_value[col_no] = self.current_player_value[col_no] - self.opponent_player_value[col_no]

            if self.col_is_full[col_no] == True:
                self.total_player_value[col_no] = -999999

             

            

        return (np.argmax(self.total_player_value) + 1, max(self.total_player_value))
        

    def play_move_2(self, game_state, current_player):
        self.game_state = game_state 
        self.current_player = current_player
        self.opponet_player = self.set_opponent_player()
        (self.no_of_rows, self.no_of_coloumns) = game_state.shape

        self.current_player_value = [-0.001 for _ in range(self.no_of_coloumns)]
        self.current_player_row = ['x' for _ in range(self.no_of_coloumns)]


        #This checks which coloumns actually have space.
        for col_no in range(self.no_of_coloumns):
            for x in range(len(self.game_state[:,col_no])):
                if self.game_state[x,col_no] == 0:
                    self.current_player_value[col_no] = 'o'
                    self.current_player_row[col_no] = x

        for col_no in range(self.no_of_coloumns):
            if self.current_player_value[col_no] == 'o':
                self.current_player_value[col_no] = self.calculate_current_player_value2(self.current_player_row[col_no], col_no)
          
        #print(self.current_player_value)
            

        return np.max(self.current_player_value) 
        
       

    def calculate_current_player_value(self, x, y):
        horizontal_to_left = 0
        horizontal_to_right = 0
        vertical_above = 0
        vertical_below = 0
        diagonal_top_left = 0
        diagonal_bottom_right = 0
        diagonal_top_right = 0
        diagonal_bottom_left= 0
        
        x_temp = x
        y_temp = y

        while True:
            if y_temp == 0: 
                break
            y_temp = y_temp - 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                horizontal_to_left += 1
            else: 
                break
            if horizontal_to_left > 2:
                break

        x_temp = x
        y_temp = y

        while True:
            if y_temp == self.no_of_coloumns - 1: 
                break
            y_temp = y_temp + 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                horizontal_to_right += 1
            else: 
                break
            if horizontal_to_right > 2:
                break

        x_temp = x
        y_temp = y

        while True:
            if x_temp == 0: 
                break
            x_temp = x_temp - 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                vertical_above += 1
            else: 
                break
            if vertical_above > 2:
                break

        x_temp = x
        y_temp = y

        while True:
            if x_temp == self.no_of_rows - 1: 
                break
            x_temp = x_temp + 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                vertical_below += 1
            else: 
                break
            if vertical_below > 2:
                break

        x_temp = x
        y_temp = y

        while True:
            if x_temp == 0 or y_temp==0: 
                break
            x_temp = x_temp - 1
            y_temp = y_temp - 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                diagonal_top_left += 1
            else: 
                break
            if diagonal_top_left > 2:
                break

        x_temp = x
        y_temp = y

        while True:
            if x_temp == 0 or y_temp==self.no_of_coloumns-1: 
                break
            x_temp = x_temp - 1
            y_temp = y_temp + 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                diagonal_top_right += 1
            else: 
                break
            if diagonal_top_right > 2:
                break

        x_temp = x
        y_temp = y
        
        while True:
            if x_temp == self.no_of_rows-1 or y_temp==self.no_of_coloumns-1: 
                break
            x_temp = x_temp + 1
            y_temp = y_temp + 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                diagonal_bottom_right += 1
            else: 
                break
            if diagonal_bottom_right > 2:
                break

        x_temp = x
        y_temp = y
        
        while True:
            if x_temp == self.no_of_rows-1 or y_temp==0: 
                break
            x_temp = x_temp + 1
            y_temp = y_temp - 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                diagonal_bottom_left += 1
            else: 
                break
            if diagonal_bottom_left > 2:
                break

        horizontal_range = horizontal_to_left + horizontal_to_right + 1
        vertical_range = vertical_above + vertical_below + 1
        diagonal_1_range = diagonal_top_right + diagonal_bottom_left + 1
        diagonal_2_range = diagonal_top_left + diagonal_bottom_right + 1

        v_score = 0
        v_score_multiplier = 1.1**self.depth

        y_temp = y - horizontal_to_left
        for c in range(horizontal_range):
            if c + 4 > horizontal_range:
                    break
            no_of_player_tokens = 0
            for f in range(4):
                #print(x_temp)
                if self.game_state[x, y_temp + c + f] == self.current_player:
                    no_of_player_tokens += 1
            
            if no_of_player_tokens == 0:
                v_score += 2
            elif no_of_player_tokens == 1:
                v_score +=3
            elif no_of_player_tokens == 2:
                v_score +=6
            elif no_of_player_tokens == 3:
                v_score += 100000
                
                
            
        x_temp = x - vertical_above

        for c in range(vertical_range):
            if c + 4 > vertical_range:
                    break
            no_of_player_tokens = 0
            for f in range(4):
                if self.game_state[x_temp + c + f, y] == self.current_player:
                    no_of_player_tokens += 1
            
            if no_of_player_tokens == 0:
                v_score += 2
            elif no_of_player_tokens == 1:
                v_score +=3
            elif no_of_player_tokens == 2:
                v_score +=6
            elif no_of_player_tokens == 3:
                v_score += 100000


        y_temp = y - diagonal_bottom_left
        x_temp = x + diagonal_bottom_left

        for c in range(diagonal_1_range):
            if c + 4 > diagonal_1_range:
                    break
            no_of_player_tokens = 0
            for f in range(4):
                if self.game_state[x_temp-c-f, y_temp + c + f] == self.current_player:
                    no_of_player_tokens += 1
            
            if no_of_player_tokens == 0:
                v_score += 2
            elif no_of_player_tokens == 1:
                v_score +=3
            elif no_of_player_tokens == 2:
                v_score +=6
            elif no_of_player_tokens == 3:
                v_score += 100000

        y_temp = y - diagonal_top_left
        x_temp = x - diagonal_top_left

        for c in range(diagonal_2_range):
            if c + 4 > diagonal_2_range:
                    break
            no_of_player_tokens = 0
            for f in range(4):
                if self.game_state[x_temp+c+f, y_temp + c + f] == self.current_player:
                    no_of_player_tokens += 1
            
            if no_of_player_tokens == 0:
                v_score += 2
            elif no_of_player_tokens == 1:
                v_score +=3
            elif no_of_player_tokens == 2:
                v_score +=6
            elif no_of_player_tokens == 3:
                v_score += 100000
        
                
                

        
        #print(y,horizontal_to_left, horizontal_to_right)        
      
        return v_score / v_score_multiplier
    

    def calculate_current_player_value2(self, x, y):
        
        horizontal_to_left = 0
        horizontal_to_right = 0
        vertical_above = 0
        vertical_below = 0
        diagonal_top_left = 0
        diagonal_bottom_right = 0
        diagonal_top_right = 0
        diagonal_bottom_left= 0
        
        x_temp = x
        y_temp = y

        while True:
            if y_temp == 0: 
                break
            y_temp = y_temp - 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                horizontal_to_left += 1
            else: 
                break
            if horizontal_to_left > 2:
                break

        x_temp = x
        y_temp = y

        while True:
            if y_temp == self.no_of_coloumns - 1: 
                break
            y_temp = y_temp + 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                horizontal_to_right += 1
            else: 
                break
            if horizontal_to_right > 2:
                break

        x_temp = x
        y_temp = y

        while True:
            if x_temp == 0: 
                break
            x_temp = x_temp - 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                vertical_above += 1
            else: 
                break
            if vertical_above > 2:
                break

        x_temp = x
        y_temp = y

        while True:
            if x_temp == self.no_of_rows - 1: 
                break
            x_temp = x_temp + 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                vertical_below += 1
            else: 
                break
            if vertical_below > 2:
                break

        x_temp = x
        y_temp = y

        while True:
            if x_temp == 0 or y_temp==0: 
                break
            x_temp = x_temp - 1
            y_temp = y_temp - 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                diagonal_top_left += 1
            else: 
                break
            if diagonal_top_left > 2:
                break

        x_temp = x
        y_temp = y

        while True:
            if x_temp == 0 or y_temp==self.no_of_coloumns-1: 
                break
            x_temp = x_temp - 1
            y_temp = y_temp + 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                diagonal_top_right += 1
            else: 
                break
            if diagonal_top_right > 2:
                break

        x_temp = x
        y_temp = y
        
        while True:
            if x_temp == self.no_of_rows-1 or y_temp==self.no_of_coloumns-1: 
                break
            x_temp = x_temp + 1
            y_temp = y_temp + 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                diagonal_bottom_right += 1
            else: 
                break
            if diagonal_bottom_right > 2:
                break

        x_temp = x
        y_temp = y
        
        while True:
            if x_temp == self.no_of_rows-1 or y_temp==0: 
                break
            x_temp = x_temp + 1
            y_temp = y_temp - 1
            if self.game_state[x_temp, y_temp] == self.current_player or self.game_state[x_temp, y_temp] == 0:
                diagonal_bottom_left += 1
            else: 
                break
            if diagonal_bottom_left > 2:
                break

        horizontal_range = horizontal_to_left + horizontal_to_right + 1
        vertical_range = vertical_above + vertical_below + 1
        diagonal_1_range = diagonal_top_right + diagonal_bottom_left + 1
        diagonal_2_range = diagonal_top_left + diagonal_bottom_right + 1

        v_score = 0

        y_temp = y - horizontal_to_left
        for c in range(horizontal_range):
            if c + 4 > horizontal_range:
                    break
            no_of_player_tokens = 0
            for f in range(4):
                #print(x_temp)
                if self.game_state[x, y_temp + c + f] == self.current_player:
                    no_of_player_tokens += 1
            
            if no_of_player_tokens == 0:
                v_score += 2
            elif no_of_player_tokens == 1:
                v_score +=3
            elif no_of_player_tokens == 2:
                v_score +=4
            elif no_of_player_tokens == 3:
                v_score += 1000
                
                
            
        x_temp = x - vertical_above

        for c in range(vertical_range):
            if c + 4 > vertical_range:
                    break
            no_of_player_tokens = 0
            for f in range(4):
                if self.game_state[x_temp + c + f, y] == self.current_player:
                    no_of_player_tokens += 1
            
            if no_of_player_tokens == 0:
                v_score += 2
            elif no_of_player_tokens == 1:
                v_score +=3
            elif no_of_player_tokens == 2:
                v_score +=4
            elif no_of_player_tokens == 3:
                v_score += 1000


        y_temp = y - diagonal_bottom_left
        x_temp = x + diagonal_bottom_left

        for c in range(diagonal_1_range):
            if c + 4 > diagonal_1_range:
                    break
            no_of_player_tokens = 0
            for f in range(4):
                if self.game_state[x_temp-c-f, y_temp + c + f] == self.current_player:
                    no_of_player_tokens += 1
            
            if no_of_player_tokens == 0:
                v_score += 2
            elif no_of_player_tokens == 1:
                v_score +=3
            elif no_of_player_tokens == 2:
                v_score +=4
            elif no_of_player_tokens == 3:
                v_score += 1000

        y_temp = y - diagonal_top_left
        x_temp = x - diagonal_top_left

        for c in range(diagonal_2_range):
            if c + 4 > diagonal_2_range:
                    break
            no_of_player_tokens = 0
            for f in range(4):
                if self.game_state[x_temp+c+f, y_temp + c + f] == self.current_player:
                    no_of_player_tokens += 1
            
            if no_of_player_tokens == 0:
                v_score += 2
            elif no_of_player_tokens == 1:
                v_score +=3
            elif no_of_player_tokens == 2:
                v_score +=4
            elif no_of_player_tokens == 3:
                v_score += 1000
        
                
                

        #print(y,horizontal_to_left, horizontal_to_right)        
      
        return v_score
    

    
    def set_opponent_player(self):
        if self.current_player == 1:
            return 2
        else:
            return 1    

