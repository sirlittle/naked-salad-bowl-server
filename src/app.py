import os

import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request
app = Flask(__name__)

db = None

def firestore_db():
    if True:
        firestore_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'server_credentials.json')
        cred = credentials.Certificate(firestore_config_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    return db

@app.route('/')
def hello_world():
    return 'BRO CHAT EXISTS'


@app.route('/create_game')
def create_game():
    return request.args.get('arg1')


@app.route('/join_room/<room_id>')
def join_room(room_id: str):
    db = firestore_db()
    rooms = db.collection('rooms').where("roomName", "==", room_id).stream()
    for room in rooms:
        print(room.id, room.to_dict())
    return 'hi'


@app.route('/<room_id>/submit_word_sets/')
def submit_word_sets(room_id):
    pass
""" 
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
 """
