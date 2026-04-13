import duckdb as db


def up(conn: db.DuckDBPyConnection) -> None:
    conn.execute(
        """
        CREATE TABLE products (
            id TEXT PRIMARY KEY DEFAULT nextval('serial'),
            name TEXT NOT NULL,
            price_frequency TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.execute("PRAGMA create_fts_index('products', 'id', 'name');")

    pass
