from marshmallow import Schema, fields, validates, ValidationError

class ConsultaSchema(Schema):
    id = fields.Int(dump_only=True)
    data = fields.Date(required=True, error_messages={"required": "Data é obrigatória."})
    hora = fields.Time(required=True, error_messages={"required": "Hora é obrigatória."})
    
    status = fields.Str(
        load_default="Agendada",
        dump_default="Agendada"
    )
    
    tipo = fields.Str(
        required=True,
        validate=lambda x: x in ['presencial', 'online'],
        error_messages={"required": "Tipo é obrigatório. Escolha entre 'presencial' ou 'online'."}
    )
    
    paciente_id = fields.Int(required=True, error_messages={"required": "Paciente é obrigatório."})
    profissional_id = fields.Int(required=True, error_messages={"required": "Profissional é obrigatório."})

    @validates('status')
    def validate_status(self, value, **kwargs):
        if value not in ('Agendada', 'Cancelada', 'Concluída'):
            raise ValidationError("Status deve ser: 'Agendada', 'Cancelada' ou 'Concluída'.")
