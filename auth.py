from flask import Blueprint, Flask, flash, redirect, render_template, request, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_mail import Mail, Message

from models.user import User


auth = Blueprint('auth', __name__)

bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()


# Inicialización del sistema de inicio de sesión
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        user = User(username=username, email=email, password=hashed_password)
        user.create()

        flash('Usuario registrado con éxito. Por favor, inicia sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Inicio de sesión fallido. Verifica tus credenciales.', 'danger')

    return render_template('login.html')

@auth.route('/profile')
@login_required
def profile():
    return 'Bienvenido, {}'.format(current_user.username)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
