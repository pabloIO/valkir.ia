from flask import Flask, render_template
from flask_socketio import SocketIO
from config.config import env

app = Flask(__name__, template_folder='public')
app.config['SECRET_KEY'] = 'c3ds1bN@de'
socketio = SocketIO(app)

@app.route("/")
def main():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print(message)


if __name__ == '__main__':
    # print(env)
    print(str.format('CONECTADO EN PUERTO {0}', env['PORT']))
    socketio.run(app, host=env['HOST'], port=env['PORT'], debug=True)