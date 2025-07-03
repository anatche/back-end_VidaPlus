from flask import Flask
from extensions import db, ma
from config import DevelopmentConfig
from error_handlers import register_error_handlers
from flask_cors import CORS  # ✅ IMPORTAÇÃO CORS

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    app.url_map.strict_slashes = False

    CORS(app)  # ✅ HABILITA CORS PARA TODAS AS ROTAS

    # Importação dos Blueprints
    from routes.paciente_routes import paciente_bp
    from routes.profissional_routes import profissional_bp
    from routes.auth_routes import auth_bp 
    from routes.consulta_routes import consulta_bp

    # Registro dos Blueprints com prefixos
    app.register_blueprint(paciente_bp, url_prefix='/pacientes')
    app.register_blueprint(profissional_bp, url_prefix='/profissionais')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(consulta_bp, url_prefix='/consultas')

    register_error_handlers(app)

    @app.route('/')
    def home():
        return "VidaPlus Backend funcionando!"

    # Exibir rotas registradas no terminal
    print("\nRotas registradas:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:25s} {list(rule.methods)} {rule}")

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        from models.paciente import Paciente
        from models.profissional_model import Profissional
        from models.consulta_model import Consulta
        db.create_all()
    app.run(debug=True)
