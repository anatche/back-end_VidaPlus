from flask import Blueprint, request, jsonify
from services.profissional_service import criar_profissional, listar_profissionais, buscar_profissional, deletar_profissional, login_profissional, trocar_senha_profissional

profissional_bp = Blueprint('profissionais', __name__, url_prefix='/profissionais')

@profissional_bp.route('/', methods=['POST'])  # <-- barra obrigatória
def criar():
    data = request.get_json()
    profissional = criar_profissional(data)
    return jsonify(profissional), 201

@profissional_bp.route('/', methods=['GET'])
def listar():
    profissionais = listar_profissionais()
    return jsonify(profissionais), 200

@profissional_bp.route('/<int:id>', methods=['GET'])
def buscar(id):
    profissional = buscar_profissional(id)
    if profissional:
        return jsonify(profissional), 200
    return jsonify({"mensagem": "Profissional não encontrado."}), 404

@profissional_bp.route('/<int:id>', methods=['DELETE'])
def deletar(id):
    sucesso = deletar_profissional(id)
    if sucesso:
        return jsonify({"mensagem": "Profissional deletado com sucesso."}), 200
    return jsonify({"mensagem": "Profissional não encontrado."}), 404

@profissional_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    resultado = login_profissional(data)
    if resultado["sucesso"]:
        return jsonify({"mensagem": "Login bem-sucedido."}), 200
    else:
        return jsonify({"mensagem": "Credenciais inválidas."}), 401

@profissional_bp.route('/<int:id>/trocar-senha', methods=['PATCH'])
def trocar_senha(id):
    data = request.get_json()
    sucesso = trocar_senha_profissional(id, data)
    if sucesso:
        return jsonify({"mensagem": "Senha alterada com sucesso."}), 200
    else:
        return jsonify({"mensagem": "Falha ao alterar a senha."}), 400
