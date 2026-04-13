import app.data as dataset
import app.database as db

_BATCH_SIZE = 100


class IngestProductsResult:
    def __init__(self, inserted: int):
        self.inserted = inserted


async def ingest_products(filepath: str) -> IngestProductsResult:
    try:
        products = await dataset.get_products_names()
        conn = db.get_db()

        to_insert = []

        existing_names = [
            row[0] for row in conn.execute("SELECT name FROM products").fetchall()
        ]

        for product in products:
            if not product in existing_names:
                to_insert.append(product)

        inserted = 0

        conn.begin()

        for i in range(0, len(to_insert), _BATCH_SIZE):
            batch = to_insert[i : i + _BATCH_SIZE]
            conn.executemany(
                "INSERT INTO products (name, price_frequency) VALUES (?, ?, ?)",
                [(p,) for p in batch],
            )
            inserted += len(batch)

        conn.commit()
        conn.close()

        return IngestProductsResult(inserted)
    except Exception as e:
        raise Exception(f"Error ingesting products: {e}")


async def ingest_daily_prices(filepath: str) -> tuple[int, int]:
    pass
