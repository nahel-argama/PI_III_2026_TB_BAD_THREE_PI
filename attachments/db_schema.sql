CREATE TYPE tipo_documento_enum AS ENUM ('CPF', 'CNPJ');
CREATE TYPE status_pedido_enum AS ENUM ('PENDENTE', 'CONFIRMADO', 'CANCELADO', 'ENTREGUE');

CREATE TABLE usuario (
  id_usuario BIGSERIAL PRIMARY KEY,
  nome VARCHAR(150) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  senha TEXT NOT NULL,
  criado_em TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE produtor (
  id_usuario BIGINT PRIMARY KEY,
  tipo_documento tipo_documento_enum NOT NULL,
  documento_numero VARCHAR(20) UNIQUE NOT NULL,
  nome_fantasia VARCHAR(150),
  FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE varejista (
  id_usuario BIGINT PRIMARY KEY,
  documento VARCHAR UNIQUE NOT NULL,
  nome_fantasia VARCHAR NOT NULL,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE endereco (
  id_endereco BIGSERIAL PRIMARY KEY,
  id_usuario BIGINT,
  rua VARCHAR NOT NULL,
  numero VARCHAR,
  complemento TEXT,
  bairro VARCHAR NOT NULL,
  cidade VARCHAR,
  estado CHAR(2) NOT NULL,
  cep VARCHAR,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),

);

CREATE TABLE categoria (
  id_categoria SERIAL PRIMARY KEY,
  nome VARCHAR UNIQUE NOT NULL,
  ativo BOOLEAN NOT NULL
);

CREATE TABLE produto (
  id_produto BIGSERIAL PRIMARY KEY,
  id_categoria INT,
  id_produtor BIGINT,
  nome VARCHAR NOT NULL,
  descricao TEXT NOT NULL,
  preco NUMERIC NOT NULL,
  quantidade_total NUMERIC NOT NULL,
  quantidade_reservada NUMERIC,
  ativo BOOLEAN NOT NULL,
  criado_em TIMESTAMP DEFAULT (CURRENT_TIMESTAMP,
  FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),
  FOREIGN KEY (id_produtor) REFERENCES produtor(id_usuario)
);

CREATE TABLE pedido (
  id_pedido BIGSERIAL PRIMARY KEY,
  id_varejista BIGINT,
  status status_pedido_enum NOT NULL,
  valor_total NUMERIC NOT NULL,
  criado_em TIMESTAMP NOT NULL,
  FOREIGN KEY (id_varejista) REFERENCES varejista(id_usuario)
);

CREATE TABLE item_pedido (
  id_item BIGSERIAL PRIMARY KEY,
  id_pedido BIGINT,
  quantidade NUMERIC NOT NULL,
  preco_unitario NUMERIC NOT NULL,
  FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
);

CREATE TABLE avaliacao (
  id_avaliacao BIGSERIAL PRIMARY KEY,
  id_pedido BIGINT,
  id_produto BIGINT,
  id_produtor BIGINT,
  id_varejista BIGINT,
  nota INT NOT NULL,
  comentario TEXT,
  criado_em TIMESTAMP NOT NULL,
  FOREIGN KEY (id_varejista) REFERENCES varejista(id_varejista),
  FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
  FOREIGN KEY (id_produto) REFERENCES produto(id_produto),
  FOREIGN KEY (id_produtor) REFERENCES produtor(id_usuario)
);