# Escoamento de Produção para Pequenos Produtores API (Django)

API REST para gerenciamento de sistema de produção entre pequenos produtores e varejistas.

---

# Como rodar o projeto

```bash
git clone https://github.com/nahel-argama/PI_III_2026_TB_BAD_THREE_PI.git
cd your-repo

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

* `POST /api/auth/login/` → Authenticate user (returns token)
* `POST /api/auth/refresh/` → Refresh token
* `POST /api/auth/verify/` → Verify token

---

# Rotas

## Users

* `POST /api/users/` → Create user
* `GET /api/users/:id/` → Get user data
* `PUT /api/users/:id/` → Update user (complete)
* `PATCH /api/users/:id/` → Update user (partial)

---

## Produtor

* `POST /api/producers/` → Create producer
* `GET /api/producers/:user_id/` → Get producer data
* `PUT /api/producers/:user_id/` → Update producer
* `PATCH /api/producers/:user_id/` → Update producer (partial)

---

## Varejista

* `POST /api/retailers/` → Create retailer
* `GET /api/retailers/:user_id/` → Get retailer data
* `PUT /api/retailers/:user_id/` → Update retailer
* `PATCH /api/retailers/:user_id/` → Update retailer (partial)

---

## Endereço

* `GET /api/addresses/` → List addresses
* `POST /api/addresses/` → Create address
* `GET /api/addresses/:id/` → Get address
* `PUT /api/addresses/:id/` → Update address
* `PATCH /api/addresses/:id/` → Update address (partial)
* `DELETE /api/addresses/:id/` → Delete address

---

## Categorias

* `GET /api/categories/` → List categories
* `POST /api/categories/` → Create category
* `GET /api/categories/:id/` → Get category
* `PUT /api/categories/:id/` → Update category
* `PATCH /api/categories/:id/` → Update category (partial)

---

## Produtos

* `GET /api/products/` → List products
* `POST /api/products/` → Create product
* `GET /api/products/:id/` → Get product
* `PUT /api/products/:id/` → Update product
* `PATCH /api/products/:id/` → Update product (partial)

---

## Pedido

* `GET /api/orders/` → List orders
* `POST /api/orders/` → Create order
* `GET /api/orders/:id/` → Get order
* `PUT /api/orders/:id/` → Update order
* `PATCH /api/orders/:id/` → Update order (partial)
* `GET /api/orders/:id/items/` → Get order items

---

## Item do Pedido

* `GET /api/order-items/` → List order items
* `POST /api/order-items/` → Create order item
* `GET /api/order-items/:id/` → Get order item
* `PUT /api/order-items/:id/` → Update order item
* `PATCH /api/order-items/:id/` → Update order item (partial)

---

## Avaliação

* `GET /api/reviews/` → List reviews
* `POST /api/reviews/` → Create review
* `GET /api/reviews/:id/` → Get review
* `PUT /api/reviews/:id/` → Update review
* `PATCH /api/reviews/:id/` → Update review (partial)

---