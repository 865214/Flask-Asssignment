from flask import Flask, request, render_template, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random 
from string import ascii_uppercase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
sockeio = SocketIO(app)
rooms = {}
def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code

@app.route('/', methods = ['GET', 'POST'])
def home():
    session.clear()
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        join = request.form.get('join', False)
        create = request.form.get('create', False)
        
        if not name:
            return render_template('home.html', error = 'Please Enter a name', name = name, code = code)
        if join != False and not code:
            return render_template('home.html', error = 'Please enter a room code', name = name , code = code)
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {'members': 0, 'messages': {}}
        elif code not in room:
            return render_template('home.html', error = 'Room does not exists', name = name , code = code)
        session['room'] = room
        session['name'] = name  
        return redirect(url_for('room'))  
    return render_template('home.html')
@app.route('/room')
def room():
    room = session.get('room')
    if room is None or session.get('name') is None or room not in rooms:
        return redirect(url_for('home'))
    return render_template('room.html', code = room)
@sockeio.on('message')
def message(data):
    room = session.get('room')
    if room not in rooms:
        return
    content = {"name" : session.get('name'),
        "message" : data["data"]}
    send(content, to = room)
    rooms[room]['messages'].append(content)
    print(f"{session.get('name')} said: {data['data']}")
@sockeio.on('connect')
def connect(auth):
      room = session.get('room')
      name = session.get('name')
      if not room and not name:
          return 
      if room not in rooms:
          leave_room(room)
          return
      join_room(room) 
      send({'name': name, 'message':"has entered the room"}, to=room)
      rooms[room]['members'] += 1
      print(f'{name} joined room {room}')  
@sockeio.on('disconnect')
def disconnect():
    room = session.get('room')
    name = session.get('name')
    if rooms[room]['members']<= 0:
        del rooms[room]
    send({'name': name, 'message': 'has left the room'}, to = room)
    print(f'{name} has left the {room}')
if __name__ == '__main__':
    sockeio.run(app, debug=True)