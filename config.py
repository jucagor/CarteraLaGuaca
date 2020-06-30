import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config():   
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'laguaca.db')

    SECRET_KEY='LLAVE SECRETA'
    DEBUG = True
    HOST='0.0.0.0'
    PORT='80'