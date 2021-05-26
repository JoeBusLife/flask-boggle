from flask import Flask, request, render_template, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

from boggle import Boggle
boggle_game = Boggle()

app = Flask(__name__)

app.config['SECRET_KEY'] = "yo"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG_TB_ENABLED'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def show_home_page():
    """ Show board size selection form """
    sizes = [[2, ""], [3, ""], [4, "Official letter mix"], [5, "Official letter mix"]]
    
    return render_template('home.html', sizes=sizes)

@app.route('/game')
def start_game():
    """ 
    -Show random board of the selcted size
    -Show form to submit a guess
    -Show current game and past game info
    """
    size = int(request.args.get('size', session.get('size', 5)))
    session['size'] = size
    session['board'] = boggle_game.make_board(size)
    board = session['board']
    
    session['scores'] = session.get('scores', [[],[],[],[],[]])
    scores = session['scores']
    
    plays = len(scores[size-1])
    high_score = max(scores[size-1]) if plays else 0
    
    return render_template('game.html', board=board, high_score=high_score, plays=plays)

@app.route('/guess', methods=['POST'])
def check_guess():
    """ Check a guessed word """
    board = session['board']
    guess = request.json.get('guess')
    guessRes = boggle_game.check_valid_word(board, guess)
    return jsonify({'result': guessRes})

@app.route('/game/over', methods=['POST'])
def log_game():
    """ Add score from finished game to session """
    score = request.json.get('score')
    scores = session['scores']
    scores[session['size']-1].append(score)
    session['scores'] = scores
    
    return jsonify("hi")