CREATE TYPE tipo_documento_enum AS ENUM ('CPF', 'CNPJ');
CREATE TYPE status_pedido_enum AS ENUM ('PENDENTE', 'CONFIRMADO', 'CANCELADO', 'ENTREGUE');

CREATE TABLE usuario (
  id_usuario BIGSERIAL PRIMARY KEY,
  nome VARCHAR,
  email VARCHAR UNIQUE,
  senha TEXT,
  criado_em TIMESTAMP
);

CREATE TABLE produtor (
  id_usuario BIGINT PRIMARY KEY,
  tipo_documento tipo_documento_enum,
  documento VARCHAR UNIQUE,
  nome_fantasia VARCHAR,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE varejista (
  id_usuario BIGINT PRIMARY KEY,
  documento VARCHAR UNIQUE,
  nome_fantasia VARCHAR,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE estado (
  id_estado SERIAL PRIMARY KEY,
  nome VARCHAR,
  sigla CHAR(2) UNIQUE
);

CREATE TABLE endereco (
  id_endereco BIGSERIAL PRIMARY KEY,
  id_usuario BIGINT,
  rua VARCHAR,
  numero VARCHAR,
  complemento TEXT,
  bairro VARCHAR,
  cidade VARCHAR,
  cep VARCHAR,
  id_estado INT,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
  FOREIGN KEY (id_estado) REFERENCES estado(id_estado)
);

CREATE TABLE categoria (
  id_categoria SERIAL PRIMARY KEY,
  nome VARCHAR UNIQUE,
  ativo BOOLEAN
);

CREATE TABLE produto (
  id_produto BIGSERIAL PRIMARY KEY,
  id_categoria INT,
  id_produtor BIGINT,
  nome VARCHAR,
  descricao TEXT,
  quantidade_total NUMERIC,
  quantidade_reservada NUMERIC,
  ativo BOOLEAN,
  criado_em TIMESTAMP,
  FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),
  FOREIGN KEY (id_produtor) REFERENCES produtor(id_usuario)
);

CREATE TABLE oferta (
  id_oferta BIGSERIAL PRIMARY KEY,
  id_produto BIGINT,
  preco NUMERIC,
  quantidade_ofertada NUMERIC,
  quantidade_disponivel NUMERIC,
  ativo BOOLEAN,
  criado_em TIMESTAMP,
  FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);

CREATE TABLE pedido (
  id_pedido BIGSERIAL PRIMARY KEY,
  id_varejista BIGINT,
  status status_pedido_enum,
  valor_total NUMERIC,
  criado_em TIMESTAMP,
  FOREIGN KEY (id_varejista) REFERENCES varejista(id_usuario)
);

CREATE TABLE item_pedido (
  id_item BIGSERIAL PRIMARY KEY,
  id_pedido BIGINT,
  id_oferta BIGINT,
  quantidade NUMERIC,
  preco_unitario NUMERIC,
  FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
  FOREIGN KEY (id_oferta) REFERENCES oferta(id_oferta)
);

CREATE TABLE avaliacao (
  id_avaliacao BIGSERIAL PRIMARY KEY,
  id_pedido BIGINT,
  id_produto BIGINT,
  id_produtor BIGINT,
  nota INT,
  comentario TEXT,
  criado_em TIMESTAMP,
  FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
  FOREIGN KEY (id_produto) REFERENCES produto(id_produto),
  FOREIGN KEY (id_produtor) REFERENCES produtor(id_usuario)
);