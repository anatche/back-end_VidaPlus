from marshmallow import Schema, fields, validate

class ProfissionalSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=2))
    cpf = fields.Str(required=True)
    especialidade = fields.Str(required=True)
    registro_profissional = fields.Str(required=True)
    email = fields.Email(required=True)
    telefone = fields.Str()
    
    # Campo write-only: aceita na entrada, não mostra na saída
    senha = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))

    # Campo para indicar se o profissional está no primeiro acesso
    primeiro_acesso = fields.Boolean(dump_only=True)
