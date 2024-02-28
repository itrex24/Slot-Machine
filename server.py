from game_logic import MAX_LINES, MAX_BET, MIN_BET, ROWS, COLS, symbol_count, symbol_value, check_winnings
from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/spin', methods=['POST'])
def spin():
    data = request.json
    lines = int(data['lines'])
    bet = int(data['bet'])
    columns = [random.choices(list(symbol_count.keys()), k=ROWS) for _ in range(COLS)]
    winnings, winning_lines = check_winnings(columns, lines, bet, symbol_value)
    return jsonify({
        'winnings': winnings,
        'winning_lines': winning_lines,
        'columns': columns
    })
