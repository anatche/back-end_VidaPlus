from flask import Blueprint, request, jsonify
from models.paciente import Paciente
from extensions import db
from schemas.paciente_schema import PacienteSchema
from marshmallow import ValidationError

paciente_bp = Blueprint('pacientes', __name__, url_prefix='/pacientes')

paciente_schema = PacienteSchema()
paciente_schema_partial = PacienteSchema(partial=True)  # para atualizações parciais

@paciente_bp.route('/', methods=['POST'])
def criar_paciente():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "Nenhum dado enviado"}), 400

    try:
        paciente = paciente_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"message": "Erro de validação", "errors": err.messages}), 400

    db.session.add(paciente)
    db.session.commit()
    resultado = paciente_schema.dump(paciente)
    return jsonify(resultado), 201

@paciente_bp.route('/', methods=['GET'])
def listar_pacientes():
    pacientes = Paciente.query.all()
    resultado = paciente_schema.dump(pacientes, many=True)
    return jsonify(resultado), 200

@paciente_bp.route('/<int:id>', methods=['GET'])
def buscar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    resultado = paciente_schema.dump(paciente)
    return jsonify(resultado), 200

@paciente_bp.route('/<int:id>', methods=['PUT'])
def atualizar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    json_data = request.get_json()

    if not json_data:
        return jsonify({"message": "Nenhum dado enviado para atualização."}), 400

    try:
        dados_atualizados = paciente_schema_partial.load(json_data)

        for key, value in dados_atualizados.items():
            setattr(paciente, key, value)

        db.session.commit()
        resultado = paciente_schema.dump(paciente)
        return jsonify(resultado), 200

    except ValidationError as err:
        return jsonify({"message": "Erro de validação", "errors": err.messages}), 400

@paciente_bp.route('/<int:id>', methods=['DELETE'])
def deletar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    return jsonify({"message": "Paciente deletado com sucesso."}), 200
