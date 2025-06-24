from models.paciente import Paciente
from extensions import db
from sqlalchemy.exc import IntegrityError

class PacienteService:

    @staticmethod
    def listar_todos():
        return Paciente.query.all()

    @staticmethod
    def buscar_por_id(id):
        return Paciente.query.get_or_404(id)

    @staticmethod
    def criar(paciente):
        try:
            db.session.add(paciente)
            db.session.commit()
            return paciente
        except IntegrityError:
            db.session.rollback()
            raise ValueError("CPF ou email já cadastrado.")

    @staticmethod
    def atualizar(id, dados_atualizados):
        paciente = Paciente.query.get_or_404(id)

        dados_dict = dados_atualizados.__dict__.copy()
        dados_dict.pop("_sa_instance_state", None)

        for key, value in dados_dict.items():
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
        paciente = Paciente.query.get_or_404(id)
        db.session.delete(paciente)
        db.session.commit()
        return True
