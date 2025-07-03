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
    response = client.post('/profissionais/', json={
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

def test_criar_profissional_duplicado(client):
    # Cria o primeiro profissional
    response1 = client.post('/profissionais/', json={
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
    response2 = client.post('/profissionais/', json={
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
    response3 = client.post('/profissionais/', json={
        "nome": "Dra. Carla 3",
        "cpf": "333.444.555-66",
        "especialidade": "Dermatologia",
        "registro_profissional": "CRM-67892",
        "email": "carla@vida.com",  # email duplicado
        "telefone": "(11) 55555-5555",
        "senha": "senha123"
    })
    assert response3.status_code == 400

def test_listar_profissionais(client):
    # Criar dois profissionais
    client.post('/profissionais/', json={
        "nome": "Dr. A",
        "cpf": "111.111.111-11",
        "especialidade": "Ortopedia",
        "registro_profissional": "CRM-00001",
        "email": "a@vida.com",
        "telefone": "(11) 11111-1111",
        "senha": "senha1"
    })
    client.post('/profissionais/', json={
        "nome": "Dr. B",
        "cpf": "222.222.222-22",
        "especialidade": "Neurologia",
        "registro_profissional": "CRM-00002",
        "email": "b@vida.com",
        "telefone": "(11) 22222-2222",
        "senha": "senha2"
    })
    response = client.get('/profissionais/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_buscar_profissional_por_id(client):
    post_resp = client.post('/profissionais/', json={
        "nome": "Dra. Carla",
        "cpf": "333.333.333-33",
        "especialidade": "Dermatologia",
        "registro_profissional": "CRM-33333",
        "email": "carla@vida.com",
        "telefone": "(11) 33333-3333",
        "senha": "senha123"
    })
    prof_id = post_resp.get_json()["id"]
    response = client.get(f'/profissionais/{prof_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == prof_id
    assert data["nome"] == "Dra. Carla"

def test_deletar_profissional(client):
    post_resp = client.post('/profissionais/', json={
        "nome": "Dr. Deletar",
        "cpf": "444.444.444-44",
        "especialidade": "Pediatria",
        "registro_profissional": "CRM-44444",
        "email": "deletar@vida.com",
        "telefone": "(11) 44444-4444",
        "senha": "senha123"
    })
    prof_id = post_resp.get_json()["id"]
    del_resp = client.delete(f'/profissionais/{prof_id}')
    assert del_resp.status_code == 200

    # Tentar buscar de novo deve dar 404
    get_resp = client.get(f'/profissionais/{prof_id}')
    assert get_resp.status_code == 404
