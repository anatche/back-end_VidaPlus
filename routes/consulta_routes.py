from flask import Blueprint, request, jsonify
from models.consulta_model import Consulta
from schemas.consulta_schema import ConsultaSchema
from extensions import db
from datetime import datetime
from marshmallow import ValidationError

consulta_bp = Blueprint('consulta_bp', __name__, url_prefix='/consultas')
consulta_schema = ConsultaSchema()
consultas_schema = ConsultaSchema(many=True)

# Criar consulta
@consulta_bp.route('/', methods=['POST'])
def criar_consulta():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "Nenhum dado enviado"}), 400

    try:
        data = consulta_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages, "message": "Erro de validação"}), 400

    nova_consulta = Consulta(
        data=data['data'],
        hora=data['hora'],
        paciente_id=data['paciente_id'],
        profissional_id=data['profissional_id'],
        status=data.get('status', 'Agendada'),
        tipo=data['tipo']
    )

    try:
        db.session.add(nova_consulta)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao criar consulta: {str(e)}"}), 500

    return jsonify(consulta_schema.dump(nova_consulta)), 201

# Listar todas as consultas
@consulta_bp.route('/', methods=['GET'])
def listar_consultas():
    consultas = Consulta.query.all()
    return jsonify(consultas_schema.dump(consultas)), 200

# Buscar consulta por ID
@consulta_bp.route('/<int:id>', methods=['GET'])
def buscar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    return jsonify(consulta_schema.dump(consulta)), 200

# Atualizar consulta
@consulta_bp.route('/<int:id>', methods=['PUT'])
def atualizar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    json_data = request.get_json()

    if not json_data:
        return jsonify({"message": "Nenhum dado enviado"}), 400

    try:
        data = consulta_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages, "message": "Erro de validação"}), 400

    if 'data' in data:
        consulta.data = data['data']
    if 'hora' in data:
        consulta.hora = data['hora']
    if 'status' in data:
        consulta.status = data['status']
    if 'tipo' in data:
        consulta.tipo = data['tipo']
    if 'paciente_id' in data:
        consulta.paciente_id = data['paciente_id']
    if 'profissional_id' in data:
        consulta.profissional_id = data['profissional_id']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao atualizar consulta: {str(e)}"}), 500

    return jsonify(consulta_schema.dump(consulta)), 200

# Cancelar consulta (soft delete)
@consulta_bp.route('/<int:id>', methods=['DELETE'])
def cancelar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    consulta.status = 'Cancelada'

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao cancelar consulta: {str(e)}"}), 500

    return jsonify({"message": "Consulta cancelada com sucesso."}), 200
