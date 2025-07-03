from marshmallow import Schema, fields, validate

class ProfissionalSchema(Schema):
    id = fields.Int(dump_only=True)

    nome = fields.Str(
        required=True,
        validate=validate.Length(min=2, error="O nome deve ter pelo menos 2 caracteres.")
    )

    cpf = fields.Str(
        required=True,
        validate=validate.Regexp(
            r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
            error="O CPF deve estar no formato 000.000.000-00"
        )
    )

    especialidade = fields.Str(required=True)
    registro_profissional = fields.Str(required=True)

    email = fields.Email(
        required=True,
        error_messages={"invalid": "Formato de e-mail inválido."}
    )

    telefone = fields.Str()

    senha = fields.Str(
        load_only=True,
        required=True,
        validate=validate.Length(min=6, error="A senha deve ter pelo menos 6 caracteres.")
    )
