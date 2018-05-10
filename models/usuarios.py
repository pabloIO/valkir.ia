from config.config import env
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
app = env['APP']
app.config['SQLALCHEMY_DATABASE_URI'] = env['SQL_CONF']['DB_URI']
db = SQLAlchemy(app)
            
def id_generator(size=150, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(45), unique=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    _conversation_id = db.Column(db.String(255), nullable=False)
    canal_socket = db.Column(db.String(255), nullable=False, default=id_generator())

db.create_all()

