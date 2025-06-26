import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

def test_login_senha_incorreta(client):
    client.post('/profissionais', json={
        "nome": "Dr. João",
        "cpf": "555.666.777-88",
        "especialidade": "Cardiologia",
        "registro_profissional": "CRM-54321",
        "email": "joao@vida.com",
        "telefone": "(11) 88888-7777",
        "senha": "temp123"
    })
    response = client.post('/profissionais/login', json={
        "nome": "Dr. João",
        "especialidade": "Cardiologia",
        "senha": "senha_errada"
    })
    assert response.status_code == 401
    assert response.get_json()["mensagem"] == "Credenciais inválidas."

def test_criar_profissional_duplicado(client):
    # Cria o primeiro profissional
    response1 = client.post('/profissionais', json={
        "nome": "Dra. Carla",
        "cpf": "222.333.444-55",
        "especialidade": "Dermatologia",
        "registro_profissional": "CRM-67890",
        "email": "carla@vida.com",
        "telefone": "(11) 77777-7777",
        "senha": "senha123"
    })
    assert response1.status_code == 201

    # Tenta criar outro com o mesmo CPF
    response2 = client.post('/profissionais', json={
        "nome": "Dra. Carla 2",
        "cpf": "222.333.444-55",  # CPF duplicado
        "especialidade": "Dermatologia",
        "registro_profissional": "CRM-67891",
        "email": "carla2@vida.com",
        "telefone": "(11) 66666-6666",
        "senha": "senha123"
    })
    assert response2.status_code == 400

    # Tenta criar outro com o mesmo email
    response3 = client.post('/profissionais', json={
        "nome": "Dra. Carla 3",
        "cpf": "333.444.555-66",
        "especialidade": "Dermatologia",
        "registro_profissional": "CRM-67892",
        "email": "carla@vida.com",  # email duplicado
        "telefone": "(11) 55555-5555",
        "senha": "senha123"
    })
    assert response3.status_code == 400
