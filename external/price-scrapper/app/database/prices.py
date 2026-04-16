import duckdb as db

from app.database.con import get_db


def get_product_prices(
    product_id: str, from_date: str, to_date: str, limit: int = 100
) -> list[dict]:
    conn = get_db()
    query = """
    SELECT
        CAST(price AS DOUBLE) AS price,
        CAST(date AS VARCHAR) AS date,
        municipality,
        state,
        region,
        commercial_level
    FROM product_prices
    WHERE product_id = ?
    """

    params = [product_id]

    if from_date:
        query += " AND date >= ?"
        params.append(from_date)

    if to_date:
        query += " AND date <= ?"
        params.append(to_date)

    query += " ORDER BY date DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    conn.close()

    return [
        {
            "price": row[0],
            "date": row[1],
            "municipality": row[2],
            "state": row[3],
            "region": row[4],
            "commercial_level": row[5],
        }
        for row in rows
    ]
