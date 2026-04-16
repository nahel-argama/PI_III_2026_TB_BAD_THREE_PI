from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.con import search_products, get_product_prices

router = APIRouter(prefix="/api")


class SearchResponse(BaseModel):
    id: str
    name: str
    price_frequency: str | None
    created_at: str | None


class PriceRecord(BaseModel):
    price: float | None
    date: str
    municipality: str | None
    state: str | None
    region: str | None
    commercial_level: str | None


@router.get("/products/search")
def search_products_endpoint(query: str, limit: int = 10):
    if not query or len(query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query parameter is required")

    results = search_products(query, limit)
    return [SearchResponse(**r) for r in results]


@router.get("/products/{product_id}/prices")
def get_prices_endpoint(
    product_id: str, from_date: str = None, to_date: str = None, limit: int = 100
):
    prices = get_product_prices(product_id, from_date, to_date, limit)
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found for this product")

    return [PriceRecord(**p) for p in prices]
