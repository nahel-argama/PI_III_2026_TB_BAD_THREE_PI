# 💳 PI Payment Gateway

> Um fake payment gateway para testes e desenvolvimento de integrações com múltiplos meios de pagamento.

---

## 📋 Índice

- [Sobre](#sobre)
- [Stack](#stack)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Meios de Pagamento](#meios-de-pagamento)
- [Rotas e Endpoints](#rotas-e-endpoints)
- [Schemas e Validações](#schemas-e-validações)
- [Tratamento de Erros](#tratamento-de-erros)
- [Exemplos Práticos](#exemplos-práticos)
- [Estrutura do Projeto](#estrutura-do-projeto)

---

## 📌 Sobre

O **PI Payment Gateway** é um serviço de processamento de pagamentos mock (simulado) desenvolvido para o 3º PI. Ele valida requisições de pagamento de acordo com regras pré-definidas e suporta três meios de pagamento diferentes:

- **Cartão de Crédito** (Credit Card) - com validações completas de dados de cartão
- **PIX** - transferência instantânea
- **Fatura** (Invoice) - pagamento por boleto/fatura

⚠️ **Importante:** Este é um serviço simulado. Não processa pagamentos reais. Ideal para:

- Testes de integração
- Desenvolvimento local
- Simulação de cenários de erro
- Prototipagem de fluxos de pagamento

---

## 🛠️ Stack

| Dependência  | Versão   | Descrição                           |
| ------------ | -------- | ----------------------------------- |
| **FastAPI**  | ≥0.135.3 | Framework HTTP moderno e rápido     |
| **Pydantic** | ≥2.12.5  | Validação de dados baseada em tipos |
| **Uvicorn**  | ≥0.44.0  | Servidor ASGI                       |
| **Python**   | ≥3.10    | Linguagem                           |

---

## 📦 Instalação

### Pré-requisitos

- **Python 3.10+** instalado

### Passo 1: Criar o Ambiente Virtual (`venv`)

No terminal, no diretório raiz do projeto, crie o ambiente virtual:

**Linux / macOS:**
```bash
python3 -m venv venv
```

**Windows:**
```cmd
python -m venv venv
```

### Passo 2: Ativar o Ambiente Virtual

Ative o ambiente virtual para que as dependências sejam isoladas no projeto:

**Linux / macOS:**
```bash
source venv/bin/activate
```

**Windows (Prompt de Comando):**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

### Passo 3: Instalar as Dependências

Com o ambiente virtual **ativado**, instale as dependências a partir do `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Passo 4: Configurar as Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` para configurar a porta padrão (8002) e o host:

```bash
cp .env.example .env
```

---

## 🚀 Como Executar

Para rodar o servidor de desenvolvimento com hot-reload (na porta 8002 por padrão, conforme configurado no `.env` ou via parâmetro), certifique-se de que o ambiente virtual está **ativado** e execute:

```bash
uvicorn src.main:app --reload --port 8002
```

Ou execute diretamente usando o executável do ambiente virtual sem precisar ativá-lo:

**Linux / macOS:**
```bash
./venv/bin/uvicorn src.main:app --reload --port 8002
```

**Windows:**
```cmd
venv\Scripts\uvicorn src.main:app --reload --port 8002
```

O servidor estará disponível em:

- **API:** `http://localhost:8002`
- **Documentação Swagger:** `http://localhost:8002/docs`
- **Documentação ReDoc:** `http://localhost:8002/redoc`

### Comandos Úteis

Com o ambiente virtual ativado:

```bash
# Rodar sem hot-reload (produção)
uvicorn src.main:app --port 8002

# Rodar em background (Linux/macOS)
uvicorn src.main:app --reload --port 8002 &

# Ver logs mais detalhados
uvicorn src.main:app --reload --port 8002 --log-level debug
```

---

## 💰 Meios de Pagamento

O gateway suporta três meios de pagamento, cada um com características e validações específicas:

| Meio            | Campo                | Validação                                                    | Casos de Uso                |
| --------------- | -------------------- | ------------------------------------------------------------ | --------------------------- |
| **CREDIT_CARD** | `card` (obrigatório) | Número (13-16 dígitos), CVV (3-4 dígitos), validade, titular | Pagamentos imediatos        |
| **PIX**         | Nenhum               | Apenas valor > 0                                             | Transferências instantâneas |
| **INVOICE**     | Nenhum               | Apenas valor > 0                                             | Pagamentos a prazo          |

### Detalhes por Meio

#### 1️⃣ Cartão de Crédito (CREDIT_CARD)

Usado para pagamentos imediatos via cartão.

**Campo necessário:**

- `card` (obrigatório) - Objeto com dados do cartão

**Exemplo de uso:**

```json
{
    "price": 99.99,
    "payment_method": "credit_card",
    "card": {
        "holder_name": "John Doe",
        "number": "4242 4242 4242 4242",
        "expiry_month": 12,
        "expiry_year": 2027,
        "cvv": "123"
    }
}
```

#### 2️⃣ PIX

Transferência instantânea bancária brasileira.

**Campo necessário:**

- Apenas `price` e `payment_method`

**Exemplo de uso:**

```json
{
    "price": 50.0,
    "payment_method": "pix"
}
```

#### 3️⃣ Fatura (INVOICE)

Pagamento por boleto ou fatura.

**Campo necessário:**

- Apenas `price` e `payment_method`

**Exemplo de uso:**

```json
{
    "price": 150.0,
    "payment_method": "invoice"
}
```

---

## 🔌 Rotas e Endpoints

O gateway expõe dois endpoints principais:

### 1. Health Check

Verifica se o serviço está operacional.

```http
GET /health
```

**Resposta (200):**

```json
{
    "status": "ok",
    "service": "pi-payment-gateway",
    "timestamp": "2026-04-15T10:30:45.123456"
}
```

---

### 2. Processar Pagamento

Processa uma requisição de pagamento validando todas as regras.

```http
POST /payments
Content-Type: application/json
```

**Parâmetros (Body):**

| Campo            | Tipo   | Validação                                       | Exemplo       |
| ---------------- | ------ | ----------------------------------------------- | ------------- |
| `price`          | float  | > 0                                             | 99.99         |
| `payment_method` | enum   | "credit_card" \| "pix" \| "invoice"             | "credit_card" |
| `card`           | object | Obrigatório se `payment_method` = "credit_card" | {...}         |

**Resposta (200 - Sucesso):**

```json
{
    "status": "success",
    "created_at": "2026-04-15T10:30:45.123456"
}
```

**Resposta (402 - Erro de Validação de Pagamento):**

```json
{
    "status": "error",
    "message": "Erro ao processar pagamento.",
    "errors": [
        {
            "field": "card.cvv",
            "message": "Erro ao processar pagamento.",
            "value": "000"
        }
    ]
}
```

**Resposta (422 - Erro de Validação de Payload):**

```json
{
    "status": "error",
    "message": "Validation error in request payload",
    "errors": [
        {
            "field": "price",
            "message": "Input should be greater than 0",
            "value": "-10"
        }
    ]
}
```

---

## 📋 Schemas e Validações

### PaymentRequestSchema

Esquema principal de requisição de pagamento.

```python
{
  "price": float,              # Valor > 0 (obrigatório)
  "payment_method": str,       # "credit_card" | "pix" | "invoice" (obrigatório)
  "card": CardSchema | None    # Obrigatório se payment_method = "credit_card"
}
```

**Validações:**

- `price` deve ser maior que 0
- `card` é obrigatório apenas para `payment_method` = "credit_card"
- `card` não deve ser fornecido para "pix" ou "invoice"

---

### CardSchema

Esquema de dados de cartão de crédito com validações rigorosas.

```python
{
  "holder_name": str,      # Nome do titular (2+ palavras, letras apenas)
  "number": str,           # Número do cartão (13-16 dígitos)
  "expiry_month": int,     # 1-12
  "expiry_year": int,      # Ano atual até +20 anos
  "cvv": str               # 3-4 dígitos
}
```

**Validações Detalhadas:**

| Campo              | Regras                                              |
| ------------------ | --------------------------------------------------- |
| `holder_name`      | Mín. 2 palavras, apenas letras, máx. 120 caracteres |
| `number`           | 13-16 dígitos, espaços removidos automaticamente    |
| `expiry_month`     | Entre 1 e 12                                        |
| `expiry_year`      | Não pode ser anterior ao ano atual                  |
| `cvv`              | 3-4 dígitos, sem espaços                            |
| **Validade geral** | Não pode estar expirado (mês/ano)                   |
| **CVV especial**   | Não pode ser "000"                                  |

---

### PaymentResponseSchema

Esquema de resposta bem-sucedida.

```python
{
  "status": str,        # "success" | "failed" | "error"
  "created_at": str     # Timestamp ISO 8601
}
```

---

### PaymentStatus (Enum)

Estados possíveis de um pagamento:

- `success` - Pagamento processado com sucesso
- `failed` - Falha na validação de regras de negócio
- `error` - Erro genérico

---

## ⚠️ Tratamento de Erros

O gateway usa códigos HTTP padronizados para indicar o resultado das operações:

| Código  | Situação             | Descrição                               |
| ------- | -------------------- | --------------------------------------- |
| **200** | ✅ Sucesso           | Pagamento processado com sucesso        |
| **402** | ❌ Erro de Pagamento | Validação de regras de pagamento falhou |
| **422** | ❌ Erro de Validação | Payload inválido ou campos malformados  |

---

## 💡 Exemplos Práticos

### 1. Pagamento com Cartão de Crédito ✅

```bash
curl -X POST http://localhost:8002/payments \
  -H "Content-Type: application/json" \
  -d '{
    "price": 99.99,
    "payment_method": "credit_card",
    "card": {
      "holder_name": "John Doe",
      "number": "4242 4242 4242 4242",
      "expiry_month": 12,
      "expiry_year": 2027,
      "cvv": "123"
    }
  }'
```

**Resposta (200):**

```json
{
    "status": "success",
    "created_at": "2026-04-15T10:35:22.456789"
}
```

---

### 2. Pagamento com PIX ✅

```bash
curl -X POST http://localhost:8002/payments \
  -H "Content-Type: application/json" \
  -d '{
    "price": 50.00,
    "payment_method": "pix"
  }'
```

**Resposta (200):**

```json
{
    "status": "success",
    "created_at": "2026-04-15T10:36:15.789012"
}
```

---

### 3. Pagamento com Fatura ✅

```bash
curl -X POST http://localhost:8002/payments \
  -H "Content-Type: application/json" \
  -d '{
    "price": 150.00,
    "payment_method": "invoice"
  }'
```

**Resposta (200):**

```json
{
    "status": "success",
    "created_at": "2026-04-15T10:37:00.234567"
}
```

---

### 4. Erro - Valor Inválido ❌

```bash
curl -X POST http://localhost:8002/payments \
  -H "Content-Type: application/json" \
  -d '{
    "price": -10.00,
    "payment_method": "pix"
  }'
```

**Resposta (422):**

```json
{
    "status": "error",
    "message": "Validation error in request payload",
    "errors": [
        {
            "field": "price",
            "message": "Input should be greater than 0",
            "value": "-10"
        }
    ]
}
```

---

### 7. Testar com Swagger (GUI)

Abra seu navegador em: **http://localhost:8002/docs**

A documentação interativa do Swagger permite:

- Visualizar todos os endpoints
- Ver schemas de request/response
- Testar endpoints diretamente na interface
- Consultar códigos de status possíveis

---

## 📁 Estrutura do Projeto

```
payment-gateway/
├── src/
│   ├── main.py                    # Configuração da app FastAPI
│   ├── api/
│   │   ├── router.py              # Agregador de rotas
│   │   └── routes/
│   │       ├── health.py          # Endpoint /health
│   │       └── payments.py        # Endpoint /payments
│   ├── schemas/
│   │   ├── error_schema.py        # Schema de erro
│   │   └── payment/
│   │       ├── request_schema.py  # PaymentRequestSchema
│   │       ├── response_schema.py # PaymentResponseSchema
│   │       ├── exceptions.py      # PaymentValidationError
│   │       ├── credit_card/
│   │       │   └── schema.py      # CardSchema
│   │       └── enums/
│   │           ├── PaymentMethods.py
│   │           └── PaymentStatus.py
│   ├── services/
│   │   └── payment_validators.py  # Lógica de validação
│   └── utils/
│       └── error_handler.py       # Handler de erros customizado
├── tests/
│   └── __init__.py
├── pyproject.toml                 # Dependências e metadados
├── .python-version                # Versão Python recomendada
└── README.md                      # Este arquivo
```

---

**Desenvolvido para PI III 2026** | 2026
