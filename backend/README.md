# Escoamento de Produção para Pequenos Produtores API (Django)

API REST para gerenciamento de sistema de produção entre pequenos produtores e varejistas.

---

# Como rodar o projeto

```bash
git clone https://github.com/nahel-argama/PI_III_2026_TB_BAD_THREE_PI.git
cd seu-repo

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```

API disponível em:

```
http://127.0.0.1:8000/
```

---

# Autenticação

* `POST /users/` → Criar usuário
* `POST /users/login/` → Login (retorna token)

---

# Rotas

## Users

* `POST /users/` → Criar usuário
* `POST /users/login/` → Autenticar usuário
* `GET /users/{id}/` → Obter dados de um usuário
* `PUT /users/{id}/` → Atualizar usuário completo
* `PATCH /users/{id}/` → Atualizar usuário parcialmente

---

## Produtor

* `POST /produtor/` → Criar produtor
* `GET /produtor/{user}/` → Obter dados do produtor
* `PUT /produtor/{user}/` → Atualizar produtor
* `PATCH /produtor/{user}/` → Atualização parcial do produtor

---

## Varejista

* `POST /varejista/` → Criar varejista
* `GET /varejista/{id_usuario}/` → Obter dados do varejista
* `PUT /varejista/{id_usuario}/` → Atualizar varejista
* `PATCH /varejista/{id_usuario}/` → Atualização parcial do varejista

---

## Endereço

* `GET /endereco/` → Listar endereços
* `POST /endereco/` → Criar endereço
* `GET /endereco/{id}/` → Obter endereço
* `PUT /endereco/{id}/` → Atualizar endereço
* `PATCH /endereco/{id}/` → Atualização parcial do endereço
* `DELETE /endereco/{id}/` → Remover endereço

---

## Categorias

* `GET /categorias/` → Listar categorias
* `POST /categorias/` → Criar categoria
* `GET /categorias/{id_categoria}/` → Obter categoria
* `PUT /categorias/{id_categoria}/` → Atualizar categoria
* `PATCH /categorias/{id_categoria}/` → Atualização parcial da categoria

---

## Produtos

* `GET /produtos/` → Listar produtos
* `POST /produtos/` → Criar produto
* `GET /produtos/{id_produto}/` → Obter produto
* `PUT /produtos/{id_produto}/` → Atualizar produto
* `PATCH /produtos/{id_produto}/` → Atualização parcial do produto

---

## Pedido

* `GET /pedido/` → Listar pedidos
* `POST /pedido/` → Criar pedido
* `GET /pedido/{id}/` → Obter pedido
* `PUT /pedido/{id}/` → Atualizar pedido
* `PATCH /pedido/{id}/` → Atualização parcial do pedido

---

## Item do Pedido

* `GET /item_pedido/` → Listar itens de pedidos
* `POST /item_pedido/` → Criar item de pedido
* `GET /item_pedido/{id}/` → Obter item
* `PUT /item_pedido/{id}/` → Atualizar item
* `PATCH /item_pedido/{id}/` → Atualização parcial do item

---

## Avaliação

* `GET /avaliacao/` → Listar avaliações
* `POST /avaliacao/` → Criar avaliação
* `GET /avaliacao/{id}/` → Obter avaliação
* `PUT /avaliacao/{id}/` → Atualizar avaliação
* `PATCH /avaliacao/{id}/` → Atualização parcial da avaliação

---