from functools import wraps
from flask import request, jsonify
import jwt
from models.user import User

SECRET_KEY = "sua_chave_secreta_aqui"  # use a mesma do auth_routes

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Pega o token do cabeçalho Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'Token JWT é obrigatório'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Usuário inválido'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
