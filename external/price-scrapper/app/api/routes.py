import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import app.database as db
import app.api.products as products

router = APIRouter(prefix="/api")


class SearchResponse(BaseModel):
    model_config = {"extra": "ignore"}

    id: str
    name: str
    presentation_name: str | None
    created_at: datetime.datetime


class PriceResponse(BaseModel):
    model_config = {"extra": "ignore"}

    product_id: str
    from_date: datetime.date
    to_date: datetime.date
    name: str
    state: str
    avg_price: float
    price_entries: dict[datetime.date, float]


@router.get("/products/search")
def search_products_endpoint(query: str, limit: int = 10):
    if not query or len(query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query parameter is required")

    normalized_query = products.normalize_query(query)

    results = db.product_search(normalized_query, limit)
    return [SearchResponse(**r) for r in results]


@router.get("/products/{product_id}/prices")
def get_prices_endpoint(
    product_id: str,
    from_date: datetime.datetime,
    to_date: datetime.datetime,
    state: str,
):
    prices = db.get_product_prices(product_id, from_date, to_date, state)
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for this product")

    avg_price = products.get_products_price_avg(prices)
    product = db.get_product_by_id(product_id)

    return PriceResponse(
        from_date=from_date,
        to_date=to_date,
        product_id=product_id,
        name=product["name"],
        state=state,
        avg_price=avg_price,
    )


@router.get("/products/{product_id}")
def get_product_endpoint(product_id: str):
    product = db.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return SearchResponse(**product)
