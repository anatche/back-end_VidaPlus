import pytest
from app import create_app
from extensions import db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_atualizar_paciente_parcial(client):
    # Criar paciente
    data = {
        "nome": "João",
        "idade": 30,
        "cpf": "123.456.789-10",
        "telefone": "11988887777",
        "email": "joao@email.com"
    }
    response = client.post('/pacientes/', json=data)
    paciente_id = response.get_json()['id']

    # Atualizar telefone só
    update_data = {"telefone": "11999990000"}
    response = client.put(f'/pacientes/{paciente_id}', json=update_data)
    assert response.status_code == 200
    json_resp = response.get_json()
    assert json_resp['telefone'] == "11999990000"
    assert json_resp['nome'] == "João"  # Verifica que nome permanece igual

def test_deletar_paciente(client):
    data = {
        "nome": "Maria",
        "idade": 25,
        "cpf": "987.654.321-00",
        "telefone": "11977776666",
        "email": "maria@email.com"
    }
    response = client.post('/pacientes/', json=data)
    paciente_id = response.get_json()['id']

    response = client.delete(f'/pacientes/{paciente_id}')
    assert response.status_code == 200
    assert "deletado" in response.get_json()['message'].lower()

    # Deletar de novo, espera 404
    response = client.delete(f'/pacientes/{paciente_id}')
    assert response.status_code == 404

def test_get_paciente_inexistente(client):
    response = client.get('/pacientes/99999')  # ID inexistente
    assert response.status_code == 404
    assert "não encontrado" in response.get_json()['message'].lower()

def test_cpf_mal_formatado(client):
    data = {
        "nome": "Carlos",
        "idade": 40,
        "cpf": "12345678900",  # Formato errado
        "telefone": "11999990000",
        "email": "carlos@email.com"
    }
    response = client.post('/pacientes/', json=data)
    assert response.status_code in (400, 422)
    assert "cpf" in str(response.get_json()).lower()

def test_email_invalido(client):
    data = {
        "nome": "Ana",
        "idade": 22,
        "cpf": "111.222.333-44",
        "telefone": "11988885555",
        "email": "anaemail.com"  # E-mail errado, falta @
    }
    response = client.post('/pacientes/', json=data)
    assert response.status_code in (400, 422)
    assert "email" in str(response.get_json()).lower()
