import duckdb as db

from app.database.con import get_db


class PriceFrequency:
    DAILY = "daily"
    MONTHLY = "monthly"


def refresh_products_fts_index(conn: db.DuckDBPyConnection) -> None:
    try:
        conn.execute("PRAGMA drop_fts_index('products')")
        conn.execute("PRAGMA create_fts_index('products', 'id', 'name')")
    except Exception as e:
        raise Exception(f"Error refreshing FTS index: {e}")


def fts_product_search(query: str, limit: int = 100) -> list[dict]:
    conn = get_db()

    pass
