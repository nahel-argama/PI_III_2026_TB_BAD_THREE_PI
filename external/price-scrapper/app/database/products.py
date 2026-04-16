import duckdb as db

from app.database.con import get_db


class PriceFrequency:
    DAILY = "daily"
    MONTHLY = "monthly"
    BOTH = "both"


def refresh_products_fts_index(conn: db.DuckDBPyConnection) -> None:
    try:
        conn.execute(
            """
            PRAGMA create_fts_index('products', 'id', 'name',
                stemmer='portuguese',
                strip_accents=1,
                lower=1,
                overwrite=1,
                ignore='[().,;:/\\-]'
            )
            """
        )
    except Exception as e:
        raise Exception(f"Error refreshing FTS index: {e}")


def fts_product_search(query: str, limit: int = 100) -> list[dict]:
    conn = get_db()
    try:
        result = conn.execute(
            """
            SELECT
                CAST(p.id AS VARCHAR) AS id,
                p.name,
                p.price_frequency,
                CAST(p.created_at AS VARCHAR) AS created_at
            FROM products p
            WHERE fts_main_products.match_bm25(p.id, ?) IS NOT NULL
            ORDER BY p.name ASC
            LIMIT ?
            """,
            [query, limit],
        )

        rows = result.fetchall()
        columns = [desc[0] for desc in result.description]

        return [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()


def get_products_by_frequency(price_frequency: str) -> list[dict]:
    """Get all products by frequency (handles 'both' frequency for price lookups)."""
    conn = get_db()
    try:
        if price_frequency == PriceFrequency.BOTH:
            result = conn.execute(
                "SELECT CAST(id AS VARCHAR) AS id, name FROM products WHERE price_frequency = ?",
                [PriceFrequency.BOTH],
            )
        else:
            result = conn.execute(
                "SELECT CAST(id AS VARCHAR) AS id, name FROM products WHERE price_frequency IN (?, ?)",
                [price_frequency, PriceFrequency.BOTH],
            )
        rows = result.fetchall()
        return [dict(zip(["id", "name"], row)) for row in rows]
    finally:
        conn.close()
