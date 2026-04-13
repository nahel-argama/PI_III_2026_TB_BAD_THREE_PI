import duckdb as db

from app.database.con import get_db


def get_product_prices(
    product_id: str, from_date: str, to_date: str, limit: int = 100
) -> list[dict]:
    conn = get_db()

    pass
