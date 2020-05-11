import os

import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request
from functools import wraps
from typing import Dict
import enum

app = Flask(__name__)

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


@app.route('/create_room')
def create_room():
    username = request.args.get('userName')
    room_name = request.args.get('roomName')
    password = request.args.get('password')

    rooms = list(db.collection('rooms').where('roomName', '==', room_name).stream())
    if len(rooms) != 0:
        return {
            'response_type': ResponseType.CREATE_ROOM_ERROR, 
            'error_msg': f'Room with name {room_name} already exists'
        }
    
    _, room = db.collection('rooms').add({'userName': userName, 'roomName': roomName, 'password': password})
    return {
        'response_type': ResponseType.SUCCESS,
        'room_id': room.id
    }
    

@app.route('/join_room/')
def join_room():
    username = request.args.get('userName')
    room_name = request.args.get('roomName')
    password = request.args.get('password')

    rooms = list(db.collection('rooms').where('roomName', '==', room_name).stream())
    if len(rooms) == 0:
        return {
            'response_type': ResponseType.JOIN_ROOM_ERROR, 
            'error_msg': f'no room named {room_name}'
        }
    if len(rooms) > 1:
        return {
            'response_type': ResponseType.JOIN_ROOM_ERROR, 
            'error_msg': f'multiple rooms named {room_name} exist'
        }

    room_id, room = rooms[0].id, rooms[0].to_dict()
    if password != room['password']:
        return {
            'response_type': ResponseType.JOIN_ROOM_ERROR, 
            'error_msg': f'Incorrect Password for room {room_name}'
        }
    return {
        'response_type': ResponseType.SUCCESS,
        'room_id': room_id
    }


@app.route('/<room_id>/submit_word_sets/')
def submit_word_sets(room_id):
    pass
""" 
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
 """
