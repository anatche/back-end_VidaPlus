from models.paciente import Paciente
from extensions import db
from sqlalchemy.exc import IntegrityError

class PacienteService:

    @staticmethod
    def listar_todos():
        """Retorna todos os pacientes cadastrados."""
        return Paciente.query.all()

    @staticmethod
    def buscar_por_id(id):
        """Busca um paciente pelo ID ou retorna 404."""
        return Paciente.query.get_or_404(id)

    @staticmethod
    def criar(data):
        cpf_existente = Paciente.query.filter_by(cpf=data['cpf']).first()
        email_existente = Paciente.query.filter_by(email=data['email']).first()

        if cpf_existente or email_existente:
            raise ValueError("CPF ou email já cadastrado")

        paciente = Paciente(**data)
        db.session.add(paciente)
        db.session.commit()
        return paciente

    @staticmethod
    def atualizar(id, update_data):
        """Atualiza os dados de um paciente existente."""
        paciente = Paciente.query.get_or_404(id)

        for key, value in update_data.items():
            setattr(paciente, key, value)

        try:
            db.session.commit()
            return paciente
        except IntegrityError:
            db.session.rollback()
            raise ValueError("CPF ou email já cadastrado.")
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e))

    @staticmethod
    def deletar(id):
        """Remove um paciente do banco de dados."""
        paciente = Paciente.query.get_or_404(id)
        db.session.delete(paciente)
        db.session.commit()
        return True
