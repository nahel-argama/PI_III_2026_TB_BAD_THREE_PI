import app.data as dataset
import app.database as db
from app.database.products import PriceFrequency

_BATCH_SIZE = 100


class IngestProductsResult:
    def __init__(self, inserted: int):
        self.inserted = inserted


def _ingest_products(products: list[dict]) -> IngestProductsResult:
    conn = db.get_db()

    to_insert = []

    existing_names = _get_existing_product_names(conn)
    staged_names = set()

    for product in products:
        name = product["name"]
        if name not in existing_names and name not in staged_names:
            to_insert.append(product)
            staged_names.add(name)

    inserted = 0

    conn.begin()

    for i in range(0, len(to_insert), _BATCH_SIZE):
        batch = to_insert[i : i + _BATCH_SIZE]
        conn.executemany(
            "INSERT INTO products (name, price_frequency) VALUES (?, ?)",
            [(p["name"], p["price_frequency"]) for p in batch],
        )
        inserted += len(batch)

    conn.commit()

    if inserted > 0:
        db.refresh_products_fts_index(conn)

    conn.close()

    return IngestProductsResult(inserted)


def _get_existing_product_names(conn) -> set[str]:
    rows = conn.execute("SELECT name FROM products").fetchall()
    return {row[0] for row in rows}


def _get_product_id_map(conn, price_frequency: str) -> dict[str, str]:
    rows = conn.execute(
        "SELECT id, name FROM products WHERE price_frequency IN (?, ?)",
        [price_frequency, PriceFrequency.BOTH],
    ).fetchall()

    return {row[1]: str(row[0]) for row in rows}


def _get_existing_price_keys(conn) -> set[tuple[str, str, str, str, str]]:
    rows = conn.execute(
        "SELECT product_id, CAST(date AS VARCHAR), municipality, state, source FROM product_prices"
    ).fetchall()

    return {
        (
            str(row[0]),
            row[1],
            row[2] or "",
            row[3] or "",
            row[4] or "",
        )
        for row in rows
    }


def _insert_price_rows(conn, rows: list[tuple]) -> int:
    inserted = 0

    for i in range(0, len(rows), _BATCH_SIZE):
        batch = rows[i : i + _BATCH_SIZE]
        conn.executemany(
            """
            INSERT INTO product_prices
            (product_id, price, date, municipality, state, region, commercial_level, metric_unit, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            batch,
        )
        inserted += len(batch)

    return inserted


async def ingest_products(daily_filepath: str, monthly_filepath: str) -> dict:
    try:
        products = await dataset.get_products_names_merged(daily_filepath, monthly_filepath)
        result = _ingest_products(products)

        return {"inserted": result.inserted}
    except Exception as e:
        raise Exception(f"Error ingesting products: {e}")


async def ingest_daily_prices(filepath: str) -> dict:
    try:
        conn = db.get_db()
        conn.begin()

        df = await dataset.get_daily_data_frame_from_csv(filepath)
        products_by_name = _get_product_id_map(conn, PriceFrequency.DAILY)
        existing_keys = _get_existing_price_keys(conn)

        to_insert = []
        skipped = 0

        for row in df.itertuples(index=False):
            product_name = row.dsc_produto
            product_id = products_by_name.get(product_name)

            if not product_id:
                skipped += 1
                continue

            date_str = row.data_preco.date().isoformat()
            key = (
                product_id,
                date_str,
                (row.municipio_ceasa or "").strip(),
                (row.uf_ceasa or "").strip(),
                PriceFrequency.DAILY,
            )

            if key in existing_keys:
                skipped += 1
                continue

            to_insert.append(
                (
                    product_id,
                    float(row.preco_diario) if row.preco_diario is not None else None,
                    date_str,
                    row.municipio_ceasa,
                    row.uf_ceasa,
                    row.dsc_ceasa,
                    row.sig_unidade_medida,
                    "daily",
                    PriceFrequency.DAILY,
                )
            )
            existing_keys.add(key)

        inserted = _insert_price_rows(conn, to_insert)
        conn.commit()
        conn.close()

        return {
            "inserted": inserted,
            "skipped": skipped,
            "total": len(df),
        }
    except Exception as e:
        raise Exception(f"Error ingesting daily prices: {e}")


async def ingest_monthly_prices(filepath: str) -> dict:
    try:
        conn = db.get_db()
        conn.begin()

        df = await dataset.get_month_data_frame_from_csv(filepath)
        products_by_name = _get_product_id_map(conn, PriceFrequency.MONTHLY)
        existing_keys = _get_existing_price_keys(conn)

        to_insert = []
        skipped = 0

        for row in df.itertuples(index=False):
            product_name = row.dsc_produto
            product_id = products_by_name.get(product_name)

            if not product_id:
                skipped += 1
                continue

            date_str = row.data_preco.date().isoformat()
            key = (
                product_id,
                date_str,
                (row.municipio_ceasa or "").strip(),
                (row.uf_ceasa or "").strip(),
                PriceFrequency.MONTHLY,
            )

            if key in existing_keys:
                skipped += 1
                continue

            to_insert.append(
                (
                    product_id,
                    float(row.preco_mensal) if row.preco_mensal is not None else None,
                    date_str,
                    row.municipio_ceasa,
                    row.uf_ceasa,
                    row.dsc_ceasa,
                    "kg",
                    "monthly",
                    PriceFrequency.MONTHLY,
                )
            )
            existing_keys.add(key)

        inserted = _insert_price_rows(conn, to_insert)
        conn.commit()
        conn.close()

        return {
            "inserted": inserted,
            "skipped": skipped,
            "total": len(df),
        }
    except Exception as e:
        raise Exception(f"Error ingesting monthly prices: {e}")
