from app import create_app
from extensions import db

app = create_app()

try:
    with app.app_context():
        db.create_all()
        print("Banco criado com sucesso!")
except Exception as e:
    print(f"Erro ao criar o banco: {e}")