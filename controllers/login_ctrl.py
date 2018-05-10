import sys
import os.path
import json 
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from models import usuarios
from sqlalchemy.exc import IntegrityError
import uuid
from config.config import env
from config.mongo_adapter import mongo

class LoginCtrl(object):
    @staticmethod
    def login(db, request, response):
        try:
            res = {
                'success': False,
            }
            exists = usuarios.Usuarios.query.filter_by(
                nombre_usuario=request['username']
            ).first()
            if exists:
                res['success'] = True
                res['id'] = exists.id
                res['username'] = exists.nombre_usuario
                res['token'] = uuid.uuid4().hex,
                res['socket_channel'] = exists.canal_socket,
                res['_conversation_id'] = exists._conversation_id 
            else:
                if not request['username']:
                    res['msg'] = 'Debes introducir el nombre de usuario'
                    return response(json.dumps(res), mimetype='application/json')
                newUser = usuarios.Usuarios(
                    nombre_usuario=request['username'],
                    canal_socket=uuid.uuid4().hex,
                    _conversation_id=str(mongo.create_conversation())
                )
                db.session.add(newUser)
                db.session.commit()
                res['success'] = True
                res['id'] = newUser.id
                res['username'] = newUser.nombre_usuario
                res['token'] = uuid.uuid4().hex
                res['socket_channel'] = newUser.canal_socket,
                res['_conversation_id'] = newUser._conversation_id 
        except Exception as e:
            print(e)
            db.session.rollback()
            res['msg'] = 'Nombre de usuario existente'
        finally:
            return response(json.dumps(res), mimetype='application/json')

        
