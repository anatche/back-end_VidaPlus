from flask import Blueprint, request, jsonify
from models.profissional_model import Profissional
from schemas.profissional_schema import ProfissionalSchema
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

profissional_bp = Blueprint('profissional_bp', __name__, url_prefix='/profissionais')
profissional_schema = ProfissionalSchema()
profissionais_schema = ProfissionalSchema(many=True)

# Criar profissional
@profissional_bp.route('/', methods=['POST'])
def criar():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "Nenhum dado enviado"}), 400

    try:
        data = profissional_schema.load(json_data)
    except Exception as e:
        return jsonify({"message": "Erro de validação", "errors": str(e)}), 400

    if Profissional.query.filter((Profissional.cpf == data['cpf']) | (Profissional.email == data['email'])).first():
        return jsonify({"message": "CPF ou email já cadastrado"}), 400

    novo_profissional = Profissional(
        nome=data['nome'],
        cpf=data['cpf'],
        especialidade=data['especialidade'],
        registro_profissional=data['registro_profissional'],
        email=data['email'],
        telefone=data['telefone'],
        senha=generate_password_hash(data['senha'])
    )

    db.session.add(novo_profissional)
    db.session.commit()

    return jsonify(profissional_schema.dump(novo_profissional)), 201

# Listar todos os profissionais
@profissional_bp.route('/', methods=['GET'])
def listar():
    profissionais = Profissional.query.all()
    return jsonify(profissionais_schema.dump(profissionais)), 200

# Buscar profissional por ID
@profissional_bp.route('/<int:id>', methods=['GET'])
def buscar(id):
    profissional = Profissional.query.get(id)
    if not profissional:
        return jsonify({"message": "Profissional não encontrado"}), 404
    return jsonify(profissional_schema.dump(profissional)), 200

# Atualizar profissional
@profissional_bp.route('/<int:id>', methods=['PUT'])
def atualizar(id):
    profissional = Profissional.query.get(id)
    if not profissional:
        return jsonify({"message": "Profissional não encontrado"}), 404

    data = request.get_json()

    profissional.nome = data.get('nome', profissional.nome)
    profissional.especialidade = data.get('especialidade', profissional.especialidade)
    profissional.registro_profissional = data.get('registro_profissional', profissional.registro_profissional)
    profissional.telefone = data.get('telefone', profissional.telefone)
    if 'senha' in data:
        profissional.senha = generate_password_hash(data['senha'])

    db.session.commit()
    return jsonify(profissional_schema.dump(profissional)), 200

# Deletar profissional
@profissional_bp.route('/<int:id>', methods=['DELETE'])
def deletar(id):
    profissional = Profissional.query.get(id)
    if not profissional:
        return jsonify({"message": "Profissional não encontrado"}), 404

    db.session.delete(profissional)
    db.session.commit()
    return jsonify({"message": "Profissional deletado com sucesso"}), 200

# Login do profissional
@profissional_bp.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "Nenhum dado enviado"}), 400

    email = json_data.get("email")
    senha = json_data.get("senha")

    profissional = Profissional.query.filter_by(email=email).first()
    if not profissional or not check_password_hash(profissional.senha, senha):
        return jsonify({"message": "Email ou senha inválidos"}), 401

    return jsonify({"message": f"Bem-vindo(a), {profissional.nome}!"}), 200
