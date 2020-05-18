import os
import time
import enum

import firebase_admin
import functools
from firebase_admin import credentials, firestore
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit
from typing import Dict

from nsb_server.gamestate.game import Game

app = Flask(__name__)
cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
app.host = "localhost"

@functools.lru_cache(maxsize=10)
def get_game(room_id):
    room = db.collection('rooms').document(room_id).get()
    if room.exists:
        room = room.to_dict()

        current_turn_guesses = [Guess(guess) for guess in room.pop('current_turn_guesses')]
        bowl = NakedSaladBowl(room.pop('unguessed_cards'), room.pop('guessed_cards'), current_turn_guesses)
        return Game(room_id=room_id, bowl=bowl, **room)
    raise KeyError()

class ResponseType(str, enum.Enum):
    SUCCESS = 'SUCCESS'
    CREATE_ROOM_ERROR = 'CREATE_ROOM_ERROR'
    JOIN_ROOM_ERROR = 'JOIN_ROOM_ERROR'

def firestore_db():
    firestore_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'server_credentials.json')
    cred = credentials.Certificate(firestore_config_path)
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = firestore_db()

def safe_call(func):
    '''
    Makes sure the server always returns something even if it errors
    '''
    def fn_safe(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            return 'Unknown Exception Occurred'
    return fn_safe

@app.route('/')
def hello_world():
    return 'BRO CHAT EXISTS'


def add_user_to_room(room_doc_ref, username):
    user_doc = room_doc_ref.collection('users').document(username)
    user_doc.set({'userName': username, 'join_time': time.time()})


@app.route('/create_room')
def create_room():
    """
    http://127.0.0.1:5000/create_room?roomName=blah&password=234&userName=Correa
    """
    username = request.args.get('userName')
    room_name = request.args.get('roomName')
    password = request.args.get('password')

    rooms = list(db.collection('rooms').where('roomName', '==', room_name).stream())
    if len(rooms) != 0:
        return {
            'response_type': ResponseType.CREATE_ROOM_ERROR, 
            'error_msg': f'Room with name {room_name} already exists'
        }
    
    room_doc_ref = db.collection('rooms').document(room_name)
    room_doc_ref.set({'adminName': username, 'roomName': room_name, 'password': password})
    room_doc_ref = add_user_to_room(room_doc_ref, username)
    return {
        'response_type': ResponseType.SUCCESS,
        'room_name': room_name
    }    

@app.route('/join_room')
def join_nsb_room():
    """
    http://127.0.0.1:5000/join_room?roomName=tester&password=234&userName=randomUserName

    This function checks the roomName and password, and returns the room id if the roomName and password match
    """
    username = request.args.get('userName')
    room_name = request.args.get('roomName')
    password = request.args.get('password')

    room_doc_ref = db.collection('rooms').document(room_name)
    room_doc = room_doc_ref.get()
    if not room_doc.exists:
        return {
            'response_type': ResponseType.JOIN_ROOM_ERROR, 
            'error_msg': f'no room named {room_name}'
        }

    room_id, room = room_doc.id, room_doc.to_dict()
    if password != room['password']:
        return {
            'response_type': ResponseType.JOIN_ROOM_ERROR, 
            'error_msg': f'Incorrect Password for room {room_name}'
        }
    
    add_user_to_room(room_doc_ref, username)
    return {
        'response_type': ResponseType.SUCCESS,
        'room_name': room_name
    }

@socketio.on('connect_to_room')
def connect_to_room(data):
    print(data)
    room_name = data['room_name']
    # game = get_game(room_id)
    join_room(room_name)  # this is a socket function, not a NSB function
    room_doc_ref = db.collection('rooms').document(room_name)
    room_doc = room_doc_ref.get()
    emit('room_update', room_doc.to_dict(), room=room_name)

@app.route('/<room_id>/submit_word_sets/')
def submit_word_sets(room_id):
    pass


if __name__ == '__main__':
    socketio.run(app, debug=True)
