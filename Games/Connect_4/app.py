from flask import Flask, render_template, request, redirect, url_for
import board
from beder_bot import beder_bot
import Arya_Bot
import copy

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Just routing button clicks from html page to python functions
    # Also runs on beginning of page
    #TODO comments above and function cleaning
    if request.method == 'POST':
        move_to_make = 1
        if app.config['turn'] == 2:
            num_filled_places = app.config['board'].get_filled_places()
            move_tup = app.config['arya_bot'].play_move(app.config['board'].retrieve_game_state(), 2, num_filled_places)
            move_to_make = move_tup[0]
            app.config['turn'] = 1 
        elif app.config['turn'] == 1:
            move_to_make = app.config['beder_bot'].get_next_move(app.config['board'].retrieve_game_state(), 1) + 1
            app.config['turn'] = 2
        
        Add = app.config['board'].add_to_coloumn(move_to_make)
        app.config['board']

        if Add[0] == False:
            print("Try again.") #TODO show message on frontend
        elif Add[1] == True:
            return render_template('index.html', board=app.config['board'].get_game_as_symbols(), message=f"Player wins!", num_of_col=len(app.config['board'].get_game_as_symbols()[0]))
        elif app.config['board'].is_board_full():
            return render_template('index.html', board=app.config['board'].get_game_as_symbols(), message="No more moves can be played. Big Sad. It's a tie.", num_of_col=len(app.config['board'].get_game_as_symbols()[0]))
    
    return render_template('index.html', board=app.config['board'].get_game_as_symbols(), message='', num_of_col=len(app.config['board'].get_game_as_symbols()[0]))

# Route for resetting the game
@app.route('/reset')
def reset():
    #TODO reset linkedlist
    app.config['board'].reset_board()
    return redirect(url_for('index'))

if __name__ == '__main__':
    num_play =  2
    num_rows = 6
    num_col = 7
    num_connect = 4
    connect_4_board = board.board(num_play, num_rows, num_col, num_connect)
    
    beder_bot = beder_bot(copy.copy(connect_4_board))
    Arya_Bot = Arya_Bot.Arya_Bot()

    app.config['arya_bot'] = Arya_Bot
    app.config['beder_bot'] = beder_bot
    app.config['board'] = connect_4_board
    app.config['turn'] = 1

    app.run(debug=True)