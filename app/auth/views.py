from flask import render_template, session, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm
from app.models import Usuario
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    
    if login_form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=login_form.username.data).first()
        if usuario is None or not usuario.check_password(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(usuario)

        #session['usuario'] = usuario    
        print('exito')
        #return redirect(url_for('index'))
        return redirect(url_for('main.index'))

    return render_template('login.html', **context)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))