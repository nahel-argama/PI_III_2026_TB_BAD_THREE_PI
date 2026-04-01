CREATE TYPE "document_type_enum" AS ENUM (
  'CPF',
  'CNPJ'
);

CREATE TYPE "unit_type_enum" AS ENUM (
  'UNIT',
  'KG'
);

CREATE TABLE "user" (
  "user_id" bigserial PRIMARY KEY,
  "name" varchar(150) NOT NULL,
  "email" varchar(150) UNIQUE NOT NULL,
  "password" text NOT NULL,
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "producer" (
  "user_id" bigint PRIMARY KEY,
  "document_type" document_type_enum NOT NULL,
  "document_number" varchar(20) UNIQUE NOT NULL,
  "trading_name" varchar(150)
);

CREATE TABLE "retailer" (
  "user_id" bigint PRIMARY KEY,
  "document_number" varchar(20) UNIQUE NOT NULL
);

CREATE TABLE "state" (
  "state_id" serial PRIMARY KEY,
  "name" varchar(100) NOT NULL,
  "abbreviation" char(2) UNIQUE NOT NULL
);

CREATE TABLE "city" (
  "city_id" serial PRIMARY KEY,
  "name" varchar(100) NOT NULL,
  "state_id" int NOT NULL
);

CREATE TABLE "address" (
  "address_id" bigserial PRIMARY KEY,
  "user_id" bigint NOT NULL,
  "street" varchar(150) NOT NULL,
  "number" varchar(10),
  "complement" varchar(100),
  "neighborhood" varchar(100),
  "city_id" int NOT NULL,
  "zip_code" varchar(8) NOT NULL,
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "category" (
  "category_id" serial PRIMARY KEY,
  "name" varchar(100) UNIQUE NOT NULL
);

CREATE TABLE "product" (
  "product_id" bigserial PRIMARY KEY,
  "producer_id" bigint NOT NULL,
  "category_id" int NOT NULL,
  "name" varchar(150) NOT NULL,
  "description" text,
  "unit_type" unit_type_enum NOT NULL,
  "price" numeric(10,2) NOT NULL,
  "quantity" numeric(10,2) NOT NULL,
  "active" boolean DEFAULT true,
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE UNIQUE INDEX ON "city" ("name", "state_id");

ALTER TABLE "producer" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "retailer" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "city" ADD FOREIGN KEY ("state_id") REFERENCES "state" ("state_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "address" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "address" ADD FOREIGN KEY ("city_id") REFERENCES "city" ("city_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "product" ADD FOREIGN KEY ("producer_id") REFERENCES "producer" ("user_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "product" ADD FOREIGN KEY ("category_id") REFERENCES "category" ("category_id") DEFERRABLE INITIALLY IMMEDIATE;
