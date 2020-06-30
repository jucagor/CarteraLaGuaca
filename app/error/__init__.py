from flask import Blueprint

error = Blueprint('error',__name__,url_prefix='/error')

from . import views