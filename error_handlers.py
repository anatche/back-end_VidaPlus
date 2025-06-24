from flask import jsonify
from marshmallow import ValidationError

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({"message": e.messages}), 400

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({"message": "Recurso não encontrado"}), 404

    @app.errorhandler(500)
    def handle_500_error(e):
        return jsonify({"message": "Erro interno no servidor"}), 500
    
    @app.errorhandler(400)
    def handle_400_error(e):
        return jsonify({"message": "Requisição inválida"}), 400