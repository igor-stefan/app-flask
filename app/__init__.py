from flask import Flask, redirect, request
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

from app.controllers import default, backend
