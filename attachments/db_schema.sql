CREATE TABLE users (
    id_user     BIGSERIAL    PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    email       VARCHAR(254) NOT NULL UNIQUE,
    password    VARCHAR(128) NOT NULL,
    user_type   VARCHAR(50)  NOT NULL CHECK (user_type IN ('ADMIN', 'PRODUCER', 'RETAILER')),
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    is_staff    BOOLEAN      NOT NULL DEFAULT FALSE,
    last_login  TIMESTAMP    NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);
CREATE TABLE address (
    id_address   BIGSERIAL    PRIMARY KEY,
    street       VARCHAR(150) NOT NULL,
    number       VARCHAR(10)  NOT NULL,
    complement   TEXT         NOT NULL DEFAULT '',
    neighborhood VARCHAR(100) NOT NULL,
    city         VARCHAR(100) NOT NULL,
    state        VARCHAR(2)   NOT NULL,
    postal_code  VARCHAR(10)  NOT NULL,
    latitude     NUMERIC(9,6) NULL,
    longitude    NUMERIC(9,6) NULL,
    id_user      BIGINT       NOT NULL UNIQUE REFERENCES users(id_user) ON DELETE CASCADE
);
CREATE TABLE category (
    id_category SERIAL       PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE
);
CREATE TABLE producer (
    id_producer     BIGSERIAL    PRIMARY KEY,
    document_type   VARCHAR(4)   NOT NULL CHECK (document_type IN ('CPF', 'CNPJ')),
    document_number VARCHAR(20)  NOT NULL UNIQUE,
    trade_name      VARCHAR(150) NOT NULL,
    id_user         BIGINT       NOT NULL UNIQUE REFERENCES users(id_user) ON DELETE CASCADE
);
CREATE TABLE retailer (
    id_retailer     BIGSERIAL    PRIMARY KEY,
    document_type   VARCHAR(4)   NOT NULL CHECK (document_type IN ('CPF', 'CNPJ')),
    document_number VARCHAR(20)  NOT NULL UNIQUE,
    trade_name      VARCHAR(150) NOT NULL,
    id_user         BIGINT       NOT NULL UNIQUE REFERENCES users(id_user) ON DELETE CASCADE
);
CREATE TABLE product (
    id_product        BIGSERIAL      PRIMARY KEY,
    name              VARCHAR(150)   NOT NULL,
    description       TEXT           NULL,
    total_quantity    FLOAT          NOT NULL,
    reserved_quantity FLOAT          NOT NULL,
    price             NUMERIC(10,2)  NOT NULL,
    is_active         BOOLEAN        NOT NULL DEFAULT TRUE,
    created_at        TIMESTAMP      NOT NULL DEFAULT NOW(),
    id_category       INT            NOT NULL REFERENCES category(id_category) ON DELETE CASCADE,
    id_producer       BIGINT         NOT NULL REFERENCES producer(id_producer) ON DELETE CASCADE
);
CREATE TABLE image (
    id_image    BIGSERIAL    PRIMARY KEY,
    blob        BYTEA        NOT NULL,
    mime_type   VARCHAR(100) NOT NULL DEFAULT 'application/octet-stream',
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);
CREATE TABLE product_image (
    id_product_image BIGSERIAL PRIMARY KEY,
    id_product       BIGINT    NOT NULL REFERENCES product(id_product) ON DELETE CASCADE,
    id_image         BIGINT    NOT NULL REFERENCES image(id_image) ON DELETE CASCADE,

    UNIQUE (id_product, id_image)
);
CREATE TABLE "order" (
    id_order    BIGSERIAL      PRIMARY KEY,
    status      VARCHAR(20)    NOT NULL DEFAULT 'PENDING'
                               CHECK (status IN ('PENDING', 'CONFIRMED', 'CANCELED', 'DELIVERED')),
    total_value NUMERIC(10,2)  NOT NULL DEFAULT 0,
    created_at  TIMESTAMP      NOT NULL DEFAULT NOW(),
    id_producer BIGINT         NOT NULL REFERENCES producer(id_producer) ON DELETE CASCADE,
    id_retailer BIGINT         NOT NULL REFERENCES retailer(id_retailer) ON DELETE CASCADE
);
CREATE TABLE order_item (
    id_order_item BIGSERIAL      PRIMARY KEY,
    quantity      INTEGER        NOT NULL CHECK (quantity > 0),
    unit_price    NUMERIC(10,2)  NOT NULL,
    id_order      BIGINT         NOT NULL REFERENCES "order"(id_order) ON DELETE CASCADE,
    id_product    BIGINT         NOT NULL REFERENCES product(id_product) ON DELETE CASCADE,

    UNIQUE (id_order, id_product)
);
CREATE TABLE review (
    id_review   BIGSERIAL PRIMARY KEY,
    rating      FLOAT     NOT NULL CHECK (rating >= 0 AND rating <= 5),
    comment     TEXT      NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    id_order    BIGINT    NOT NULL REFERENCES "order"(id_order) ON DELETE CASCADE
);
CREATE TABLE wishlist (
    id_wishlist BIGSERIAL PRIMARY KEY,
    id_retailer BIGINT    NOT NULL UNIQUE REFERENCES retailer(id_retailer) ON DELETE CASCADE
);
CREATE TABLE wishlist_item (
    id_wishlist_item     BIGSERIAL    PRIMARY KEY,
    product_external_key TEXT         NOT NULL,
    product_name         VARCHAR(150) NOT NULL,
    id_wishlist          BIGINT       NOT NULL REFERENCES wishlist(id_wishlist) ON DELETE CASCADE
);
CREATE TABLE wishlist_item_image (
    id_wishlist_item_image BIGSERIAL PRIMARY KEY,
    product_external_key   TEXT      NOT NULL UNIQUE,
    id_image               BIGINT    NOT NULL REFERENCES image(id_image) ON DELETE CASCADE
);