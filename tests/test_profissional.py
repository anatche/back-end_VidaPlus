import pytest
from app import create_app
from extensions import db
from models.profissional_model import Profissional

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client

def test_criar_profissional(client):
    response = client.post('/profissionais', json={
        "nome": "Dra. Ana",
        "cpf": "111.222.333-44",
        "especialidade": "Psiquiatria",
        "registro_profissional": "CRM-12345",
        "email": "ana@vida.com",
        "telefone": "(11) 99999-9999",
        "senha": "senha123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["nome"] == "Dra. Ana"
    assert data["especialidade"] == "Psiquiatria"
    assert "id" in data

def test_login_profissional(client):
    client.post('/profissionais', json={
        "nome": "Dr. João",
        "cpf": "555.666.777-88",
        "especialidade": "Cardiologia",
        "registro_profissional": "CRM-54321",
        "email": "joao@vida.com",
        "telefone": "(11) 88888-7777",
        "senha": "temp123"
    })
    login = client.post('/profissionais/login', json={
        "nome": "Dr. João",
        "especialidade": "Cardiologia",
        "senha": "temp123"
    })
    assert login.status_code == 200
    assert login.get_json()["mensagem"] == "Login bem-sucedido."
