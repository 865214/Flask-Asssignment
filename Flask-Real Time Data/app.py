from flask import Flask, render_template
from flask_socketio import SocketIO
import time
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Initial counter value
counter_value = 0

def update_counter():
    global counter_value
    while True:
        # Increment the counter every second
        time.sleep(1)
        counter_value += 1

        # Broadcast the updated counter value to all connected clients
        socketio.emit('update_counter', {'value': counter_value})

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # Start the counter update thread
    counter_thread = Thread(target=update_counter)
    counter_thread.start()

    # Run the Flask app with SocketIO
    socketio.run(app, debug=True)