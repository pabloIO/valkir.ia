from config.config import env
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import uuid
app = env['APP']
app.config['SQLALCHEMY_DATABASE_URI'] = env['SQL_CONF']['DB_URI']
db = SQLAlchemy(app)

class Sesion(db.Model):
    __tablename__ = 'sesion'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text, nullable=False, default=uuid.uuid4().hex)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ### FK from table usuarios
    usuarios_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    # usuarios = db.relationship('Usuarios',  backref=db.backref('sesion', lazy=True))

# db.create_all()

