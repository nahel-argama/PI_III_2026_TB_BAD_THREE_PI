# Escoamento de Produção para Pequenos Produtores API (Django)

API REST para gerenciamento de sistema de produção entre pequenos produtores e varejistas.

---

## Como rodar o projeto

```bash
git clone https://github.com/nahel-argama/PI_III_2026_TB_BAD_THREE_PI.git
cd your-repo

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

cp .env.example .env

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

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

## Documentação das Rotas

A documentação das rotas do projeto pode ser encontrada na pasta [collections](collections). Recomendo usar o OpenCollection para visualizar a documentação de forma interativa.
