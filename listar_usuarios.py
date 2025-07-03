from app import create_app
from extensions import db
from models.user import User

def listar_usuarios():
    app = create_app()
    with app.app_context():
        usuarios = User.query.all()
        if not usuarios:
            print("Nenhum usuário encontrado.")
        for u in usuarios:
            print(f"ID: {u.id} | Email: {u.email}")

if __name__ == "__main__":
    listar_usuarios()
