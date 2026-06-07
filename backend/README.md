# Escoamento de Produção para Pequenos Produtores API (Django)

API REST para gerenciamento de sistema de produção entre pequenos produtores e varejistas.

---

## Como rodar o projeto

Clonar o repositório

```bash
git clone https://github.com/nahel-argama/PI_III_2026_TB_BAD_THREE_PI.git
cd your-repo
```

Criar venv e instalar as dependências

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

Definir as envs

```bash
cp .env.example .env
```

Preparar o banco com docker

```bash
cp compose.dev.yml compose.yml
docker compose up --build -d
```

Preparar o banco de dados

```bash
python manage.py makemigrations
python manage.py migrate
python seed_categories.py
```

Rodar o servidor

```bash
python manage.py runserver
```

API disponível em:

```text
http://127.0.0.1:8000/
```

## Como criar um usuário admin

O projeto utiliza um usuário admin customizado.

```bash
python manage.py create_admin_user
```

Assim que criado, o usuário poderá fazer login pela mesma rota de login dos outros usuários.

## Populando com usuários de teste

```bash
python manage.py seed_users
```

Tabela de usuários:

| Email                        | Senha      | Tipo de Usuário |
|------------------------------|------------|-----------------|
| produtor.norte@example.com   | teste123   | Produtor        |
| produtor.nordeste@example.com| teste123   | Produtor        |
| produtor.centro_oeste@example.com| teste123 | Produtor        |
| produtor.sudeste@example.com | teste123   | Produtor        |
| produtor.sul@example.com     | teste123   | Produtor        |
| varejista.norte@example.com  | teste123   | Varejista       |
| varejista.nordeste@example.com| teste123  | Varejista       |
| varejista.centro_oeste@example.com| teste123| Varejista       |
| varejista.sudeste@example.com| teste123  | Varejista       |
| varejista.sul@example.com    | teste123   | Varejista       |

## Documentação das Rotas

A documentação das rotas do projeto pode ser encontrada na pasta [collections](collections). Recomendo usar o OpenCollection para visualizar a documentação de forma interativa.
