from models.profissional_model import Profissional
from extensions import db

def criar_profissional(data):
    profissional = Profissional(
        nome=data['nome'],
        cpf=data['cpf'],
        especialidade=data['especialidade'],
        registro_profissional=data['registro_profissional'],
        email=data['email'],
        telefone=data.get('telefone')
    )
    profissional.set_senha(data['senha'])
    db.session.add(profissional)
    db.session.commit()
    return profissional

def listar_profissionais():
    return Profissional.query.all()

def buscar_profissional_por_id(profissional_id):
    return Profissional.query.get_or_404(profissional_id)

def deletar_profissional(profissional_id):
    profissional = buscar_profissional_por_id(profissional_id)
    db.session.delete(profissional)
    db.session.commit()

def autenticar_profissional(nome, especialidade, senha):
    profissional = Profissional.query.filter_by(nome=nome, especialidade=especialidade).first()
    if profissional and profissional.verificar_senha(senha):
        return profissional
    return None

def atualizar_senha_profissional(profissional_id, nova_senha):
    profissional = buscar_profissional_por_id(profissional_id)
    profissional.set_senha(nova_senha)
    profissional.primeiro_acesso = False
    db.session.commit()
    return profissional
