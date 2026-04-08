from datetime import date

import duckdb as db


def get_db() -> db.DuckDBPyConnection:
    return db.connect("database/database.db")


def init_db() -> None:
    conn = get_db()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS prices (
            product TEXT,
            classification TEXT,
            product_id INTEGER,
            municipality TEXT,
            ibge_code TEXT,
            state TEXT,
            region TEXT,
            year INTEGER,
            month INTEGER,
            week_date_range TEXT,
            week_number INTEGER,
            commercial_level TEXT,
            price_per_kg DECIMAL(10, 2)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS read_history (
            id INTEGER PRIMARY KEY DEFAULT nextval('read_history_id_seq'),
            filename TEXT NOT NULL,
            read_date DATE NOT NULL,
            row_count INTEGER,
            inserted_count INTEGER,
            duration_seconds FLOAT
        )
        """
    )


def insert_new_prices_from_temp(
    conn: db.DuckDBPyConnection, temp_table_name: str
) -> int:
    conn.execute(
        f"""
        INSERT INTO prices
        SELECT * FROM {temp_table_name}
        WHERE (product_id, municipality, week_date_range) NOT IN (
            SELECT product_id, municipality, week_date_range FROM prices
        )
        """
    )

    inserted_count = conn.execute(
        f"SELECT COUNT(*) FROM {temp_table_name} WHERE (product_id, municipality, week_date_range) NOT IN (SELECT product_id, municipality, week_date_range FROM prices)"
    ).fetchone()[0]

    return inserted_count


def log_ingestion(
    conn: db.DuckDBPyConnection,
    filename: str,
    row_count: int,
    inserted_count: int,
    duration_seconds: float,
) -> None:
    conn.execute(
        """
        INSERT INTO read_history (filename, read_date, row_count, inserted_count, duration_seconds)
        VALUES (?, ?, ?, ?, ?)
        """,
        (filename, date.today(), row_count, inserted_count, duration_seconds),
    )
