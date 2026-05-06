CREATE TYPE "tipo_documento_enum" AS ENUM (
  'CPF',
  'CNPJ'
);

CREATE TYPE "status_pedido_enum" AS ENUM (
  'PENDENTE',
  'CONFIRMADO',
  'CANCELADO',
  'ENTREGUE'
);

CREATE TABLE "usuario" (
  "id_usuario" BIGSERIAL PRIMARY KEY,
  "nome" "VARCHAR(150)" NOT NULL,
  "email" "VARCHAR(150)" UNIQUE NOT NULL,
  "senha" TEXT NOT NULL,
  "criado_em" TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "produtor" (
  "id_usuario" BIGINT PRIMARY KEY,
  "tipo_documento" tipo_documento_enum NOT NULL,
  "documento_numero" "VARCHAR(20)" UNIQUE NOT NULL,
  "nome_fantasia" "VARCHAR(150)"
);

CREATE TABLE "varejista" (
  "id_usuario" BIGINT PRIMARY KEY,
  "documento" VARCHAR UNIQUE NOT NULL,
  "nome_fantasia" VARCHAR NOT NULL
);

CREATE TABLE "endereco" (
  "id_endereco" BIGSERIAL PRIMARY KEY,
  "id_usuario" BIGINT,
  "rua" VARCHAR NOT NULL,
  "numero" VARCHAR,
  "complemento" TEXT,
  "bairro" VARCHAR NOT NULL,
  "cidade" VARCHAR,
  "estado" "CHAR(2)" NOT NULL,
  "cep" VARCHAR
);

CREATE TABLE "categoria" (
  "id_categoria" SERIAL PRIMARY KEY,
  "nome" VARCHAR UNIQUE NOT NULL,
  "ativo" BOOLEAN NOT NULL
);

CREATE TABLE "produto" (
  "id_produto" BIGSERIAL PRIMARY KEY,
  "id_categoria" INT,
  "id_produtor" BIGINT,
  "nome" VARCHAR NOT NULL,
  "descricao" TEXT NOT NULL,
  "preco" NUMERIC NOT NULL,
  "quantidade_total" NUMERIC NOT NULL,
  "quantidade_reservada" NUMERIC,
  "ativo" BOOLEAN NOT NULL,
  "criado_em" TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "pedido" (
  "id_pedido" BIGSERIAL PRIMARY KEY,
  "id_varejista" BIGINT,
  "status" status_pedido_enum NOT NULL,
  "valor_total" NUMERIC NOT NULL,
  "criado_em" TIMESTAMP NOT NULL
);

CREATE TABLE "item_pedido" (
  "id_item" BIGSERIAL PRIMARY KEY,
  "id_pedido" BIGINT,
  "quantidade" NUMERIC NOT NULL,
  "preco_unitario" NUMERIC NOT NULL
);

CREATE TABLE "avaliacao" (
  "id_avaliacao" BIGSERIAL PRIMARY KEY,
  "id_pedido" BIGINT,
  "id_produto" BIGINT,
  "id_produtor" BIGINT,
  "id_varejista" BIGINT,
  "nota" INT NOT NULL,
  "comentario" TEXT,
  "criado_em" TIMESTAMP NOT NULL
);

CREATE TABLE "imagem" (
  "id_imagem" BIGSERIAL PRIMARY KEY,
  "url" TEXT NOT NULL,
  "criado_em" timestamp NOT NULL
);

CREATE TABLE "imagem_produto" (
  "id_imagem_produto" BIGSERIAL PRIMARY KEY,
  "id_imagem" BIGSERIAL NOT NULL,
  "id_produto" BIGSERIAL NOT NULL
);

ALTER TABLE "imagem_produto" ADD FOREIGN KEY ("id_produto") REFERENCES "produto" ("id_produto") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "imagem_produto" ADD FOREIGN KEY ("id_imagem") REFERENCES "imagem" ("id_imagem") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "produtor" ADD FOREIGN KEY ("id_usuario") REFERENCES "usuario" ("id_usuario") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "varejista" ADD FOREIGN KEY ("id_usuario") REFERENCES "usuario" ("id_usuario") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "endereco" ADD FOREIGN KEY ("id_usuario") REFERENCES "usuario" ("id_usuario") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "produto" ADD FOREIGN KEY ("id_categoria") REFERENCES "categoria" ("id_categoria") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "produto" ADD FOREIGN KEY ("id_produtor") REFERENCES "produtor" ("id_usuario") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "pedido" ADD FOREIGN KEY ("id_varejista") REFERENCES "varejista" ("id_usuario") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "item_pedido" ADD FOREIGN KEY ("id_pedido") REFERENCES "pedido" ("id_pedido") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "avaliacao" ADD FOREIGN KEY ("id_varejista") REFERENCES "varejista" ("id_usuario") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "avaliacao" ADD FOREIGN KEY ("id_pedido") REFERENCES "pedido" ("id_pedido") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "avaliacao" ADD FOREIGN KEY ("id_produto") REFERENCES "produto" ("id_produto") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "avaliacao" ADD FOREIGN KEY ("id_produtor") REFERENCES "produtor" ("id_usuario") DEFERRABLE INITIALLY IMMEDIATE;
