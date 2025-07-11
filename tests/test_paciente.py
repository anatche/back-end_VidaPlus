import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from models.paciente import Paciente

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # banco em memória
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_criar_paciente(client):
    data = {
        "nome": "Teste User",
        "cpf": "111.222.333-44",
        "telefone": "11999998888",
        "email": "teste.user@email.com",
        "data_nascimento": "1993-08-15"  
    }
    response = client.post('/pacientes/', json=data)
    assert response.status_code == 201
    json_resp = response.get_json()
    assert json_resp['nome'] == "Teste User"
    assert json_resp['cpf'] == "111.222.333-44"

def test_criar_paciente_duplicado(client):
    data = {
        "nome": "User Duplicado",
        "cpf": "111.222.333-44",
        "telefone": "11999991111",
        "email": "user.dup@email.com",
        "data_nascimento": "1990-05-10" 
    }
    # Cria o primeiro paciente
    client.post('/pacientes/', json=data)
    # Tenta criar de novo com o mesmo CPF
    response = client.post('/pacientes/', json=data)
    assert response.status_code == 400
    json_resp = response.get_json()
    assert "CPF ou email já cadastrado" in json_resp['message']
