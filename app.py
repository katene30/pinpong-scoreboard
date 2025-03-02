from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow WebSockets from any origin

# Global score variables for player 1 and player 2
score_player_1 = 0
score_player_2 = 0

game_state = "active"
winning_score = 21
game_point = winning_score - 1
service_interval = 5

current_server = 1

player_names = {1: "Player 1", 2: "Player 2"}


@app.route('/')
def index():
    
    return "Flask WebSocket Backend Running"

@socketio.on('connect')
def handle_connect():
    # Send the initial scores when a player connects
# TODO remove this stuff
    emit('score_update', {
        'player_1': score_player_1,
        'player_2': score_player_2,
        'server': current_server
    })

    emit('name_update', {
        "player1": player_names[1],
        "player2": player_names[2]
    })

@socketio.on('update_names')
def update_names(data):
    player_names[1] = data.get("player1", "Player 1")
    player_names[2] = data.get("player2", "Player 2")

    emit('name_update', {
        "player1": player_names[1],
        "player2": player_names[2]
    }, broadcast=True)

@socketio.on('set_server')
def set_server(data):
    """ Manually set who starts serving """
    global current_server
    current_server = data['player']
    emit('score_update', {'player_1': score_player_1, 'player_2': score_player_2, 'server': current_server}, broadcast=True)

def update_game_state():
    global game_state, game_point, service_interval, score_player_1, score_player_2

    game_point = winning_score - 1

    # Check if both players are at or above game_point
    if score_player_1 >= game_point and score_player_2 >= game_point:
        game_state = "deuce"

        service_interval = 1 if winning_score <= 15 else 2 
    else:
        game_state = "active"

    # Determine if someone has won
    if game_state == "deuce":
        if abs(score_player_1 - score_player_2) >= 2:
            game_state = "win"
    elif max(score_player_1, score_player_2) >= winning_score:
        game_state = "win"


@socketio.on('increment_score')
def handle_increment(data):
    global score_player_1, score_player_2, current_server, service_interval, game_state
    player = data.get('player')  # Expecting 'player' key to be sent with '1' or '2'
    
    if game_state == 'win':
        return

    if player == 1:
        score_player_1 += 1
    elif player == 2:
        score_player_2 += 1

    total_score = score_player_1 + score_player_2

    update_game_state()

    if total_score % service_interval == 0:
        current_server = 1 if current_server == 2 else 2
    # Broadcast updated scores to all connected clients
    emit('score_update', {
        'player_1': score_player_1,
        'player_2': score_player_2,
        'server': current_server
    }, broadcast=True)

    emit('game_state_update', {
        'gameState': game_state,
        'serviceInterval': service_interval,
        'winningScore': winning_score,
    }, broadcast=True)

@socketio.on('decrement_score')
def handle_decrement(data):
    global score_player_1, score_player_2, current_server
    player = data.get('player')  # Expecting 'player' key to be sent with '1' or '2'

    if player == 1 and score_player_1 > 0:
        score_player_1 -= 1
    elif player == 2 and score_player_2 > 0:
        score_player_2 -= 1
    else:
        return

    total_score = score_player_1 + score_player_2

    update_game_state()

    if total_score % service_interval == 0:
        current_server = 1 if current_server == 2 else 2

    # Broadcast updated scores to all connected clients
    emit('score_update', {'player_1': score_player_1, 'player_2': score_player_2, 'server': current_server}, broadcast=True)

    emit('game_state_update', {
        'gameState': game_state,
        'serviceInterval': service_interval,
        'winningScore': winning_score,
    }, broadcast=True)

@socketio.on('clear_score')
def handle_clear_score():
    global score_player_1, score_player_2, current_server
    score_player_1 = 0  # Reset player 1's score
    score_player_2 = 0  # Reset player 2's score
    current_server = 1
    service_interval = 5

    update_game_state()

    # Broadcast updated scores to all connected clients
    emit('score_update', {'player_1': score_player_1, 'player_2': score_player_2, 'server': current_server}, broadcast=True)

    emit('game_state_update', {
        'gameState': game_state,
        'serviceInterval': service_interval,
        'winningScore': winning_score,
    }, broadcast=True)

@socketio.on('clear_names')
def handle_clear_names():
    global player_names
    player_names = {1: "Player 1", 2: "Player 2"}

    # Broadcast updated names to all connected clients
    emit('name_update', {
        "player1": player_names[1],
        "player2": player_names[2]
    }, broadcast=True)
    
@socketio.on('update_winning_score')
def update_winning_score(data):
    global winning_score
    winning_score = data['winningScore']
    socketio.emit('game_state_update', {'winningScore': winning_score, 'serviceInterval': service_interval, 'gameState': game_state})

@socketio.on('update_service_interval')
def update_service_interval(data):
    global service_interval
    service_interval = data['serviceInterval']
    socketio.emit('game_state_update', {'winningScore': winning_score, 'serviceInterval': service_interval, 'gameState': game_state})

@socketio.on('switch_names')
def switch_names(data):
    global player_names
    player_names[1], player_names[2] = player_names[2], player_names[1]

    emit('name_update', {
        "player1": player_names[1],
        "player2": player_names[2]
    }, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
