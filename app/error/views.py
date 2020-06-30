from flask import render_template, request
from app import db
from app.error import error
from flask_login import current_user

@error.app_errorhandler(404)
def not_found_error(error):
    context = {
    'usuario': current_user
    }    
    return render_template('404.html',**context)