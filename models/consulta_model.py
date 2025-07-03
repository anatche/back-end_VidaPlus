from extensions import db
from models.paciente import Paciente
from models.profissional_model import Profissional

class Consulta(db.Model):
    __tablename__ = 'consultas'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='Agendada')
    tipo = db.Column(db.String(20), nullable=False)

    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=False)

    paciente = db.relationship("models.paciente.Paciente", backref="consultas", lazy=True)
    profissional = db.relationship("models.profissional_model.Profissional", backref="consultas", lazy=True)
