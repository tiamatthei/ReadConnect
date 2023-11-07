from flask import Blueprint, Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from models.user import User


auth_bp = Blueprint('auth', __name__)

bcrypt = Bcrypt()
login_manager = LoginManager()


# Inicialización del sistema de inicio de sesión
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    user = User(username=username, email=email, password=hashed_password)
    user.create()

    return jsonify({'message': 'Usuario registrado con éxito.'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Inicio de sesión exitoso.'}), 200
    else:
        return jsonify({'message': 'Inicio de sesión fallido. Verifica tus credenciales.'}), 401

@auth_bp.route('/profile')
@login_required
def profile():
    return jsonify({'message': 'Bienvenido, {}'.format(current_user.username)}), 200

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Sesión cerrada exitosamente.'}), 200
