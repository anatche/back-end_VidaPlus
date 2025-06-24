from flask import Blueprint, request, jsonify
from schemas.profissional_schema import ProfissionalSchema
from services import profissional_service

profissional_bp = Blueprint('profissionais', __name__)
prof_schema = ProfissionalSchema()
prof_schema_many = ProfissionalSchema(many=True)

@profissional_bp.route('', methods=['POST'])
def criar():
    data = request.get_json()
    profissional = profissional_service.criar_profissional(data)
    return jsonify(prof_schema.dump(profissional)), 201

@profissional_bp.route('', methods=['GET'])
def listar():
    profissionais = profissional_service.listar_profissionais()
    return jsonify(prof_schema_many.dump(profissionais))

@profissional_bp.route('/<int:id>', methods=['GET'])
def buscar(id):
    profissional = profissional_service.buscar_profissional_por_id(id)
    return jsonify(prof_schema.dump(profissional))

@profissional_bp.route('/<int:id>', methods=['DELETE'])
def deletar(id):
    profissional_service.deletar_profissional(id)
    return jsonify({"mensagem": "Profissional deletado com sucesso."}), 204

@profissional_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    profissional = profissional_service.autenticar_profissional(
        data.get('nome'),
        data.get('especialidade'),
        data.get('senha')
    )
    if profissional:
        return jsonify({
            "mensagem": "Login bem-sucedido.",
            "primeiro_acesso": profissional.primeiro_acesso
        }), 200
    return jsonify({"mensagem": "Credenciais inválidas."}), 401

@profissional_bp.route('/<int:id>/trocar-senha', methods=['PATCH'])
def trocar_senha(id):
    data = request.get_json()
    profissional = profissional_service.atualizar_senha_profissional(id, data['nova_senha'])
    return jsonify({"mensagem": "Senha atualizada com sucesso."}), 200
