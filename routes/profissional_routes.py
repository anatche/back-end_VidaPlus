from flask import Blueprint, request, jsonify
from models.profissional_model import Profissional
from schemas.profissional_schema import ProfissionalSchema
from extensions import db

profissional_bp = Blueprint('profissional_bp', __name__, url_prefix='/profissionais')
profissional_schema = ProfissionalSchema()
profissionais_schema = ProfissionalSchema(many=True)

@profissional_bp.route('/', methods=['POST'])
def criar():
    data = request.get_json()

    if Profissional.query.filter_by(cpf=data.get('cpf')).first():
        return jsonify({"message": "CPF já cadastrado."}), 400

    if Profissional.query.filter_by(email=data.get('email')).first():
        return jsonify({"message": "Email já cadastrado."}), 400

    profissional = Profissional(
        nome=data.get('nome'),
        cpf=data.get('cpf'),
        especialidade=data.get('especialidade'),
        registro_profissional=data.get('registro_profissional'),
        email=data.get('email'),
        telefone=data.get('telefone')
    )

    profissional.set_senha(data.get('senha'))

    db.session.add(profissional)
    db.session.commit()

    return jsonify(profissional_schema.dump(profissional)), 201


@profissional_bp.route('/', methods=['GET'])
def listar():
    profissionais = Profissional.query.all()
    return jsonify(profissionais_schema.dump(profissionais)), 200


@profissional_bp.route('/<int:id>', methods=['GET'])
def buscar(id):
    profissional = Profissional.query.get_or_404(id)
    return jsonify(profissional_schema.dump(profissional)), 200


@profissional_bp.route('/<int:id>', methods=['PUT'])
def atualizar(id):
    profissional = Profissional.query.get_or_404(id)
    data = request.get_json()

    if 'nome' in data:
        profissional.nome = data['nome']

    if 'cpf' in data:
        existente = Profissional.query.filter_by(cpf=data['cpf']).first()
        if existente and existente.id != id:
            return jsonify({"message": "CPF já cadastrado por outro profissional."}), 400
        profissional.cpf = data['cpf']

    if 'especialidade' in data:
        profissional.especialidade = data['especialidade']

    if 'registro_profissional' in data:
        profissional.registro_profissional = data['registro_profissional']

    if 'email' in data:
        existente = Profissional.query.filter_by(email=data['email']).first()
        if existente and existente.id != id:
            return jsonify({"message": "Email já cadastrado por outro profissional."}), 400
        profissional.email = data['email']

    if 'telefone' in data:
        profissional.telefone = data['telefone']

    if 'senha' in data:
        profissional.set_senha(data['senha'])

    db.session.commit()
    return jsonify(profissional_schema.dump(profissional)), 200


@profissional_bp.route('/<int:id>', methods=['DELETE'])
def deletar(id):
    profissional = Profissional.query.get_or_404(id)
    db.session.delete(profissional)
    db.session.commit()
    return jsonify({"message": "Profissional deletado com sucesso."}), 200


@profissional_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({"message": "Email e senha são obrigatórios"}), 400

    profissional = Profissional.query.filter_by(email=email).first()

    if not profissional or not profissional.check_senha(senha):
        return jsonify({"message": "Credenciais inválidas"}), 401

    return jsonify(profissional_schema.dump(profissional)), 200
