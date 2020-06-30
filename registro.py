from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.models import Usuario

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


usuario=Usuario(username=str(input("ingrese el nombre de usuario ")))
usuario.set_password(str(input("ingrese su contraseña ")))
usuario.email=str(input("ingrese su email "))
usuario.compañia=str(input("ingrese su compañia "))

db.session.add(usuario)
db.session.commit()

print("usuario agregago con exito")