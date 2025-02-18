from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow WebSockets from any origin

# Global score variable
score = 0

@app.route('/')
def index():
    return "Flask WebSocket Backend Running"

@socketio.on('connect')
def handle_connect():
    emit('score_update', {'score': score})

@socketio.on('increment_score')
def handle_increment():
    global score
    score += 1
    emit('score_update', {'score': score}, broadcast=True)

@socketio.on('decrement_score')
def handle_decrement():
    global score
    score -= 1
    emit('score_update', {'score': score}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
