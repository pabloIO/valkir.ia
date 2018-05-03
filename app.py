from flask import Flask, render_template
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c3ds1bN@de'
socketio = SocketIO(app)

@app.route("/")
def main():
    return "Welcome!"


if __name__ == '__main__':
    socketio.run()