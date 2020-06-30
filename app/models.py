from app import db,login
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
from flask_login import UserMixin
from datetime import datetime, timedelta

class Usuario(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    compañia = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128), default=0)
    
    def __repr__(self):
        return '<Usuario {} de la Compañia {}>'.format(self.username,self.compañia)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    tipo_identificacion = db.Column(db.String(24))
    nombre=db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    recibir_notificaciones=db.Column(db.Boolean, default=False)
    numero_tel=db.Column(db.String(64), index=True)
    direccion=db.Column(db.String(64), index=True)
    descripcion=db.Column(db.String(64), index=True)
    fecha_inscripcion=db.Column(db.DateTime, default=datetime.now())
    cliente_al_dia=db.Column(db.Boolean, default=True)
    saldo=db.Column(db.Integer, default=0)
    fecha_pago=db.Column(db.DateTime, default=None)
    facturas = db.relationship('Factura', backref='tiene_factura', lazy='dynamic')

    def __repr__(self):
        return '<{} {}>'.format(self.id,self.nombre)

class Factura(db.Model):
    id=db.Column(db.Integer, primary_key=True, unique=True)
    cliente_id=db.Column(db.Integer, db.ForeignKey(Cliente.id))
    monto=db.Column(db.Integer)
    fecha=db.Column(db.DateTime, default=datetime.now())
    vigencia=db.Column(db.DateTime)
    descripcion=db.Column(db.String(120))
    credito=db.Column(db.Boolean, default=False)
    numero_cuotas=db.Column(db.Integer, default=0)
    periodicidad_cuotas=db.Column(db.Integer, default=0)
    saldo=db.Column(db.Integer)
    al_dia=db.Column(db.Boolean, default=True)
    cancelada=db.Column(db.Boolean, default=False)
    abonos = db.relationship('Abono', backref='abono', lazy='dynamic')
    cuotas = db.relationship('Cuota', backref='cuota', lazy='dynamic')
    vendedor=db.Column(db.String(40))
    

    def __repr__(self):
        return '<Factura numero {} por monto de {}>'.format(self.id,self.monto)

class Abono(db.Model):
    id=db.Column(db.Integer, primary_key=True, unique=True)
    factura_id=db.Column(db.Integer, db.ForeignKey(Factura.id))
    monto=db.Column(db.Integer)
    fecha=db.Column(db.DateTime, default=datetime.now())
    descripcion=db.Column(db.String(120))
    abono_adicional=db.Column(db.Boolean, default=False)
    reduccion_cuotas=db.Column(db.Boolean, default=False)
    abono_capital=db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Abono numero {} por monto de {}>'.format(self.id,self.monto)

class Cuota(db.Model):
    id=db.Column(db.Integer, primary_key=True, unique=True)
    numero=db.Column(db.Integer)
    factura_id=db.Column(db.Integer, db.ForeignKey(Factura.id))
    monto=db.Column(db.Integer)
    fecha=db.Column(db.DateTime)
    cliente_id=db.Column(db.Integer, db.ForeignKey(Cliente.id))
    vencida=db.Column(db.Boolean, default=False)

@login.user_loader
def load_user(id):
    return Usuario.query.get(int(id))



    