from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow WebSockets from any origin

# Global score variables for player 1 and player 2
score_player_1 = 0
score_player_2 = 0

current_server = 1

@app.route('/')
def index():
    return "Flask WebSocket Backend Running"

@socketio.on('connect')
def handle_connect():
    # Send the initial scores when a player connects
    emit('score_update', {
        'player_1': score_player_1,
        'player_2': score_player_2,
        'server': current_server
    })

@socketio.on('increment_score')
def handle_increment(data):
    global score_player_1, score_player_2, current_server
    player = data.get('player')  # Expecting 'player' key to be sent with '1' or '2'
    

    if player == 1:
        score_player_1 += 1
    elif player == 2:
        score_player_2 += 1

    total_score = score_player_1 + score_player_2
    if total_score % 5 == 0:
        current_server = 1 if current_server == 2 else 2
    # Broadcast updated scores to all connected clients
    emit('score_update', {'player_1': score_player_1, 'player_2': score_player_2, 'server': current_server}, broadcast=True)

@socketio.on('decrement_score')
def handle_decrement(data):
    global score_player_1, score_player_2, current_server
    player = data.get('player')  # Expecting 'player' key to be sent with '1' or '2'

    if player == 1:
        score_player_1 -= 1
    elif player == 2:
        score_player_2 -= 1

    total_score = score_player_1 + score_player_2
    if total_score % 5 == 0:
        current_server = 1 if current_server == 2 else 2

    # Broadcast updated scores to all connected clients
    emit('score_update', {'player_1': score_player_1, 'player_2': score_player_2, 'server': current_server}, broadcast=True)

@socketio.on('clear_score')
def handle_clear_score():
    global score_player_1, score_player_2, current_server
    score_player_1 = 0  # Reset player 1's score
    score_player_2 = 0  # Reset player 2's score
    current_server = 1

    # Broadcast updated scores to all connected clients
    emit('score_update', {'player_1': score_player_1, 'player_2': score_player_2, 'server': current_server}, broadcast=True)
    

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
