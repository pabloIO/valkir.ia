from config.config import env
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

app = env['APP']
app.config['SQLALCHEMY_DATABASE_URI'] = env['SQL_CONF']['DB_URI']
db = SQLAlchemy(app)

class Conversacion(db.Model):
    '''
    Atribs from the table
    '''
    id = db.Column(db.Integer, primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    '''
    FK from table usuarios
    '''
    usuarios_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuarios = db.relationship('Usuarios',  backref=db.backref('conversaciones', lazy=True))
    
db.create_all()