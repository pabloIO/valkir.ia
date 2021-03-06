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
    __tablename__ = 'conversacion'
    __table_args__ = {'schema': config['SQL_CONF']['DB_NAME']}
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ### FK FROM TABLE SESSION
    sesion_id = db.Column(Integer, db.ForeignKey('sesion.id'), nullable=False)
    sesion = db.relationship('Sesion', backref=db.backref('conversacion', lazy=True))

    ### FK from table usuarios
    usuarios_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuarios = db.relationship('Usuarios',  backref=db.backref('usuarios', lazy=True))
    
db.create_all()