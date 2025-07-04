from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from schemas.paciente_schema import PacienteSchema
from services.paciente_service import PacienteService

paciente_bp = Blueprint('pacientes', __name__, url_prefix='/pacientes')

paciente_schema = PacienteSchema()
paciente_schema_partial = PacienteSchema(partial=True)  

@paciente_bp.route('/', methods=['POST'])
def criar_paciente():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "Nenhum dado enviado"}), 400

    try:
        data = paciente_schema.load(json_data)
        paciente = PacienteService.criar(data)
        return jsonify(paciente_schema.dump(paciente)), 201
    except ValidationError as err:
        return jsonify({"message": "Erro de validação", "errors": err.messages}), 400
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    
@paciente_bp.route('/', methods=['GET'])
def listar_pacientes():
    pacientes = PacienteService.listar_todos()
    return jsonify(paciente_schema.dump(pacientes, many=True)), 200

@paciente_bp.route('/<int:id>', methods=['GET'])
def buscar_paciente(id):
    paciente = PacienteService.buscar_por_id(id)
    return jsonify(paciente_schema.dump(paciente)), 200

@paciente_bp.route('/<int:id>', methods=['PUT'])
def atualizar_paciente(id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "Nenhum dado enviado para atualização."}), 400

    try:
        dados_atualizados = paciente_schema_partial.load(json_data)
        paciente = PacienteService.atualizar(id, dados_atualizados)
        return jsonify(paciente_schema.dump(paciente)), 200

    except ValidationError as err:
        return jsonify({"message": "Erro de validação", "errors": err.messages}), 400
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@paciente_bp.route('/<int:id>', methods=['DELETE'])
def deletar_paciente(id):
    PacienteService.deletar(id)
    return jsonify({"message": "Paciente deletado com sucesso."}), 200
