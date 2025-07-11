# back-end_VidaPlus
# 💙 VidaPlus - Sistema de Gestão Hospitalar e de Serviços de Saúde

Este é um sistema back-end desenvolvido em Flask para gerenciamento de pacientes, profissionais da saúde e agendamento de consultas. O projeto simula uma clínica ou hospital de pequeno porte e foi desenvolvido como Trabalho de Conclusão de Curso (TCC) no curso de Análise e Desenvolvimento de Sistemas.

## 🩺 Funcionalidades implementadas

### 👤 Pacientes
- Cadastro, listagem, busca, atualização e remoção de pacientes.
- Autenticação (login).
- Preparado para futuramente acessar histórico clínico, agendar/cancelar consultas e acessar teleconsultas.

### 🧑‍⚕️ Profissionais de Saúde
- Cadastro, listagem, busca, atualização e remoção.
- Login e troca de senha.
- Associado às consultas com pacientes.

### 📅 Consultas
- Agendamento de consulta (data, hora, paciente, profissional).
- Listagem geral e por ID.
- Atualização de status (por exemplo, para “Cancelada”).
- Relacionamento com pacientes e profissionais.

### 🔐 Autenticação (Auth)
- Sistema de login com geração de token JWT.
- Segurança de senha com hash (usando Werkzeug).

### 📦 Banco de Dados
- SQLite com SQLAlchemy.
- Relacionamentos entre tabelas implementados corretamente.
- Esquemas de serialização com Marshmallow.

### ✅ Testes
- Testes realizados com Postman.
- Testes em Pytest em desenvolvimento.

### 🌐 Interface Web (opcional)
- Página HTML simples para listar e agendar consultas usando JavaScript + fetch.
- Servida localmente com `python -m http.server`.

---

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
https://github.com/anatche/back-end_VidaPlus.git
