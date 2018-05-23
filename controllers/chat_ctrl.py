import sys
import os.path
import json 
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import models.models as database
from sqlalchemy.exc import IntegrityError
import uuid
from config.config import env
from config.mongo_adapter import mongo
from bot import valkiria, chatter
import time

class ChatCtrl(object):
    @staticmethod
    def sendResponse(db, bot, data, emit):
        try:
            ## Get response from bot
            response = chatter.Chatter.answer(bot, data['message'], data['_conversation_id'])
            ## FACTOR DE RETRASO
            delay_factor = env['CHILD_TIME_WRITING_FACTOR']            
            num_words = len(response.split(' '))
            ## tiempo calculado a responder
            time_to_respond = num_words * delay_factor
            emit('typing', {
                'userName': 'valkiria',
                },
                room=data['room'])
            ## retrasar evento typing por el tiempo
            ## time_to_respond y activar animacion
            time.sleep(time_to_respond)
            ## nueva conversacion
            newMessage = database.Conversacion(
                texto=data['message'],
                usuarios_id=data['user_id'],
                sesion_id=data['sesion_id'],
                respuesta_bot=response
            )
            db.session.add(newMessage)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            ## enviar evento stop typing
            emit('stop typing',{
                'userName': 'valkiria'
            }, 
            room=data['room'])
            ## retardar 0.4 segundos el evento stop typing
            ## para activar la animacion
            time.sleep(0.4)
            ## emitir evento user_says:msg
            emit('user_says:msg', {
                'userName': 'valkiria',
                'message': response
            }, room=data['room'])
    @staticmethod
    def getConversation(user_id, db, response):
        try:
            res = {
                'success': False
            }
            user = database.Usuarios.query.get(user_id)
            db_conversations = database.Conversacion.query.filter_by(usuarios_id=user_id).all()
            user_conversation =  []
            for conversation in db_conversations:
                print(conversation.fecha_creacion)
                c = {
                    'id': conversation.id,
                    'created_at': str(conversation.fecha_creacion),
                    'user_res': {
                        'userName': user.nombre_usuario,
                        'message': conversation.texto,
                    },
                    'bot_res': {
                        'userName': 'valkiria',
                        'message': conversation.respuesta_bot,                        
                    }
                }
                user_conversation.append(c)
            res['success'] = True            
            res['conversation'] = user_conversation
        except Exception as e:
            print(e)
            res['msg'] = 'Hubo un error al obtener la conversación'
        finally:
            print(res)
            return response(json.dumps(res), mimetype='application/json')            

        
