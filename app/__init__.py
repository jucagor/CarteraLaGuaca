from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

login=LoginManager()
login.login_view = 'auth.login'
db=SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)
    boostrap = Bootstrap(app)
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.auth import auth
    app.register_blueprint(auth)

    from app.main import main
    app.register_blueprint(main)

    from app.error import error
    app.register_blueprint(error)


    return app

from app import models

