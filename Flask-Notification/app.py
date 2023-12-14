from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('send_notification')
def handle_notification(message):
    print(f'Received notification: {message}')
    # Broadcast the notification to all connected clients
    socketio.emit('receive_notification', message)

if __name__ == '__main__':
    socketio.run(app, debug=True)