from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit, send
from config.config import env
from bot import valkiria, chatter
from flask_sqlalchemy import SQLAlchemy
from controllers import login_ctrl
# print(valkiria.Bot)
app = Flask(__name__, template_folder="public")
app.config['SECRET_KEY'] = env['APP_SECRET']
socketio = SocketIO(app)
bot = valkiria.Bot('Valkiria', 'valkiria_chatbot2')
## DATABASE CONFIG AND INSTANTIATION
app.config['SQLALCHEMY_DATABASE_URI'] = env['SQL_CONF']['DB_URI']
db = SQLAlchemy(app)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/login", methods=['POST'])
def login():
    return login_ctrl.LoginCtrl.login(db, request.form, Response)

@socketio.on('message')
def handle_message(message):
    print(message)

@socketio.on('new message')
def handle_new_message(message):
    msg = chatter.Chatter.answer(bot, message)
    print(msg)
    emit('user_says:msg', msg)

if __name__ == '__main__':
    # print(env)
    print(str.format('CONECTADO EN PUERTO {0}', env['PORT']))
    socketio.run(app, host=env['HOST'], port=env['PORT'], debug=True)