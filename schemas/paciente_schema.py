from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import validate, fields, post_load
from models.paciente import Paciente
from extensions import db
from datetime import date

class PacienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Paciente
        load_instance = True
        sqla_session = db.session

    id = fields.Int(dump_only=True)

    nome = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="O nome é obrigatório.")
    )

    cpf = fields.Str(
        required=True,
        validate=validate.Regexp(
            r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
            error="O CPF deve estar no formato 000.000.000-00"
        )
    )

    telefone = fields.Str()

    email = fields.Email(
        required=True,
        error_messages={"invalid": "Formato de e-mail inválido."}
    )

    data_nascimento = fields.Date(
        required=True,
        error_messages={"invalid": "A data deve estar no formato YYYY-MM-DD."}
    )

    idade = fields.Int(dump_only=True)

    @post_load
    def calcular_idade(self, data, **kwargs):
        if 'data_nascimento' in data:
            hoje = date.today()
            nascimento = data['data_nascimento']
            idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
            data['idade'] = idade
        return data
