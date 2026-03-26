import duckdb as db

from app.database import get_db


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


def product_search(query: str, limit: int = 100) -> list[dict]:
    fts_results = fts_product_search(query, limit)

    if fts_results:
        return fts_results

    return levenshtein_product_search(query, limit)


def fts_product_search(query: str, limit: int = 100) -> list[dict]:
    conn = get_db()
    try:
        result = conn.execute(
            """
            SELECT
                p.id,
                p.name,
                p.created_at,
                fts_main_products.match_bm25(p.id, ?) as score
            FROM products p
            WHERE score IS NOT NULL
            ORDER BY score DESC
            LIMIT ?
            """,
            [query, limit],
        )

        rows = result.fetchall()
        columns = [desc[0] for desc in result.description]

        return [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()


def levenshtein_product_search(query: str, limit: int = 100) -> list[dict]:
    conn = get_db()
    try:
        result = conn.execute(
            """
            SELECT
                p.id,
                p.name,
                p.created_at,
                levenshtein(p.name, ?) as score
            FROM products p
            WHERE score IS NOT NULL
            ORDER BY score ASC
            LIMIT ?
            """,
            [query, limit],
        )

        rows = result.fetchall()
        columns = [desc[0] for desc in result.description]

        return [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()


def get_product_by_id(product_id: str) -> dict | None:
    conn = get_db()
    try:
        result = conn.execute(
            """
            SELECT
                id,
                name,
                created_at
            FROM products
            WHERE id = ?
            """,
            [product_id],
        )

        row = result.fetchone()
        if row is None:
            return None

        columns = [desc[0] for desc in result.description]
        return dict(zip(columns, row))
    finally:
        conn.close()
