from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import validate, fields
from models.paciente import Paciente
from extensions import db  # importa o db para pegar a sessão

class PacienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Paciente
        load_instance = True
        sqla_session = db.session  # ESSENCIAL para corrigir o erro!

    id = fields.Int(dump_only=True)

    nome = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="O nome é obrigatório.")
    )

    idade = fields.Int(
        required=True,
        validate=validate.Range(min=0, max=130, error="A idade deve estar entre 0 e 130.")
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
