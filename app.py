from flask import Flask, render_template, request, Response
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit, send, join_room
from config.config import env
from bot import valkiria, chatter
from flask_sqlalchemy import SQLAlchemy
# print(valkiria.Bot)
app = Flask(__name__, template_folder="public")
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = env['APP_SECRET']
socketio = SocketIO(app)
bot = valkiria.Bot('Valkiria', 'valkiria_chatbot2')
## DATABASE CONFIG AND INSTANTIATION
app.config['SQLALCHEMY_DATABASE_URI'] = env['SQL_CONF']['DB_URI']
db = SQLAlchemy(app)

cors = CORS(app, resources={r"/login": {"origins": "http://localhost:3000"}})

addedUser = False
usernames = {}
numUsers = 0

from controllers import login_ctrl, chat_ctrl

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/chat_room")
def chat_room():
    return render_template('chatRoom.html')

@app.route("/login", methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def login():
    return login_ctrl.LoginCtrl.login(db, request.form, Response)

@app.route('/user/<user_id>/conversation')
def show_user_conversation(user_id):
    return chat_ctrl.ChatCtrl.getConversation(user_id, db, Response)
    

'''
    @socket.on event create_room: Creates individual room for user
    @param Dict data: Dictionary containing data with room number
    @return socket.send event 
'''
@socketio.on('create_room')
def handle_create_room(data):
    room = data['room']
    print('#####################')
    print('#####################')
    print('#####################')
    print(str.format('user has entered to room: {0}', room))
    print()
    print()
    print()
    print()
    join_room(room)

@socketio.on('add_user')
def handle_add_user(username):
    ## we store the username in the socket session for this client
    # socket.username = username
    global usernames
    global numUsers
    global addedUser

    addedUser = True
    print(username)
    ## add the client's username to the global list
    name = username['usr']
    if(name not in usernames.keys()):
        usernames[name] = name
        numUsers += 1
        addedUser = True

        emit('user_joined', {
        'username': name,
        'numUsers': numUsers,
        }, broadcast=True)

@socketio.on('typing')
def handle_typing(data):
    emit('typing', 
        {
            'userName': data['userName']
        }, 
        room=data['room'])

@socketio.on('stop typing')
def handle_stop_typing(data):
    emit('stop typing', 
        {
            'userName': data['userName']
        }, 
        room=data['room'])

@socketio.on('new_message')
def handle_new_message(data):
    chat_ctrl.ChatCtrl.sendResponse(db, bot, data, emit)
    # print(message)

    # msg = chatter.Chatter.answer(bot, message)
    # print(msg)
    # emit('user_says:msg', {
    #     'userName': 'valkiria',
    #     'message': msg
    # })

if __name__ == '__main__':
    # print(env)
    print(str.format('CONECTADO EN PUERTO {0}', env['PORT']))
    socketio.run(app, host=env['HOST'], port=env['PORT'], debug=True)