from flask import Flask, render_template
from flask_socketio import SocketIO


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("kill")
def kill():
    socketio.emit(
        "kill"
    )

@socketio.on("start")
def start(data):
    socketio.emit(
        "start",
        data
    )


@socketio.on("stats")
def maskCompliance(data):
    socketio.emit(
        "stats",
        data
    )

@socketio.on("cells")
def cells(data):
    print("cells")
    socketio.emit(
        "cells",
        data
    )

@socketio.on("cells_data")
def cells_data(data):
    print("cells_data")
    socketio.emit(
        "cells_data",
        data
    )

@socketio.on("message")
def message(message):
    print("message", message)
    socketio.emit("message", message)


if __name__ == '__main__':
    print("Starting server")
    socketio.run(app)