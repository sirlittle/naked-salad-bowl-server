import os
import yaml

from firebase_admin import firestore
from flask import Flask, request
app = Flask(__name__)


def firebase():
    firebase_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'firebase_config.yaml')
    with open(firebase_config_path) as f:
        contents = f.read()
        config = yaml.load(contents)
    return Firebase(config)


def get_room(room_name):
    pass
    # get from firestore
    # convert to room object
    # call method on room object


@app.route('/')
def hello_world():
    return 'BRO CHAT EXISTS'


@app.route('/create_game')
def create_game():
    return request.args.get('arg1')


@app.route('/join_room/<room_id>')
def join_room(room_id: str):
    fb = firebase()
    return room_id


@app.route('/<room_id>/submit_word_sets/')
def submit_word_sets(room_id):
    pass
""" 
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
 """
