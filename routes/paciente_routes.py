from flask import Blueprint, request, jsonify
from schemas.paciente_schema import PacienteSchema
from services.paciente_service import PacienteService
from marshmallow import ValidationError
from routes.auth_utils import token_required

paciente_bp = Blueprint('paciente_bp', __name__, url_prefix='/pacientes')

paciente_schema = PacienteSchema()
pacientes_schema = PacienteSchema(many=True)

# Listar todos os pacientes (rota protegida)
@paciente_bp.route('/', methods=['GET'])
@token_required
def listar_pacientes(current_user):
    pacientes = PacienteService.listar_todos()
    return jsonify(pacientes_schema.dump(pacientes))

# Buscar paciente por ID (rota protegida)
@paciente_bp.route('/<int:id>', methods=['GET'])
@token_required
def buscar_paciente(current_user, id):
    paciente = PacienteService.buscar_por_id(id)
    return jsonify(paciente_schema.dump(paciente))

# Criar novo paciente (rota protegida)
@paciente_bp.route('/', methods=['POST'])
@token_required
def criar_paciente(current_user):
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "Nenhum dado informado"}), 400

    try:
        paciente = paciente_schema.load(json_data)
        paciente = PacienteService.criar(paciente)
        return jsonify(paciente_schema.dump(paciente)), 201

    except ValidationError as ve:
        return jsonify({"message": "Erro de validação", "errors": ve.messages}), 400

    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400

# Atualizar paciente existente (rota protegida)
@paciente_bp.route('/<int:id>', methods=['PUT'])
@token_required
def atualizar_paciente(current_user, id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "Nenhum dado informado"}), 400

    try:
        dados_atualizados = paciente_schema.load(json_data, partial=True)
        paciente = PacienteService.atualizar(id, dados_atualizados)
        return jsonify(paciente_schema.dump(paciente)), 200

    except ValidationError as ve:
        return jsonify({"message": "Erro de validação", "errors": ve.messages}), 400

    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400

# Deletar paciente (rota protegida)
@paciente_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def deletar_paciente(current_user, id):
    PacienteService.deletar(id)
    return jsonify({"message": "Paciente deletado com sucesso!"}), 200
