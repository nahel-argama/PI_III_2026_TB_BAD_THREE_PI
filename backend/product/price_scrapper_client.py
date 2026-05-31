from dataclasses import dataclass
from typing import Generic, TypeVar, TypedDict

import requests
from rest_framework import exceptions, status

import config.settings as settings

BASE_URL = settings.PRICE_SCRAPPER_ENDPOINT
TIMEOUT_SECONDS = 10


class ProductDetailResponse(TypedDict):
    id: str
    name: str
    created_at: str


T = TypeVar("T")


@dataclass(frozen=True)
class ExternalServiceResponse(Generic[T]):
    status: int
    data: T


@dataclass(frozen=True)
class ExternalServiceError:
    message: str


def get_product_by_id(
    product_id: str,
) -> ExternalServiceResponse[ProductDetailResponse] | ExternalServiceError:
    url = f"{BASE_URL}/api/products/{product_id}"

    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
    except requests.RequestException:
        return ExternalServiceError(
            message="External service request failed",
        )

    if not response.ok:
        return ExternalServiceError(
            message=response.json()["detail"],
        )

    return ExternalServiceResponse(status=response.status_code, data=response.json())


def get_product_by_id_validated(
    product_id: str,
) -> ExternalServiceResponse[ProductDetailResponse]:
    response = get_product_by_id(product_id)

    if isinstance(response, ExternalServiceError):
        raise exceptions.APIException(
            detail=response.message, code=status.HTTP_400_BAD_REQUEST
        )

    return response
