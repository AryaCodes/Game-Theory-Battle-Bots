from flask import Flask, render_template, request, redirect, url_for
import board
from Beder import random_bot

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Just routing button clicks from html page to python functions
    # Also runs on beginning of page
    #TODO comments above and function cleaning
    if request.method == 'POST':
        move_to_make = 1
        is_bot_move = request.form.get('isBotMove')
        if(is_bot_move):
            move_to_make = random_bot.random_move(app.config['board'])
            pass
        else:
            move_to_make = int(request.form['col'])

        Add = app.config['board'].add_to_coloumn(move_to_make)
        app.config['board']

        if Add[0] == False:
            print("Try again.") #TODO show message on frontend
        elif Add[1] == True:
            return render_template('index.html', board=app.config['board'].get_game_as_symbols(), message=f"Player wins!", num_of_col=len(app.config['board'].get_game_as_symbols()[0]))
            #TODO vvv
            # print(f"Player {test.get_current_player()} has won. Congratulations!'")
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
    
    app.config['board'] = connect_4_board

    app.run(debug=True)