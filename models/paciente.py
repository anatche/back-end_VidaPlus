from extensions import db

class Paciente(db.Model):
    __tablename__ = 'pacientes'  # nome da tabela no banco

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f'<Paciente {self.nome}>'