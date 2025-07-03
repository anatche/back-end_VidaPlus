from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db
import jwt
import datetime
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

SECRET_KEY = "sua_chave_secreta_aqui"  # 🔐 Substitua por uma chave segura real

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('senha'):
        return jsonify({"message": "Email e senha são obrigatórios"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email já cadastrado"}), 400

    user = User(email=data['email'])
    user.set_password(data['senha'])  # Aceitando campo 'senha'
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuário criado com sucesso"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('senha'):
        return jsonify({"message": "Email e senha são obrigatórios"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['senha']):  # Aceitando 'senha'
        return jsonify({"message": "Credenciais inválidas"}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token}), 200
