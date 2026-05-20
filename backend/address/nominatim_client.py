from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

import requests

NOMINATIM_SEARCH_URL = "https://nominatim.openstreetmap.org/search"
TIMEOUT_SECONDS = 10
USER_AGENT = "production-flow-api/1.0"
COORDINATE_PRECISION = Decimal("0.000001")


@dataclass(frozen=True)
class Coordinates:
    latitude: Decimal
    longitude: Decimal


@dataclass(frozen=True)
class GeocodingError:
    message: str


def build_address_query(address_data: dict[str, Any]) -> str:
    street = address_data.get("street")
    number = address_data.get("number")
    street_line = " ".join(str(value).strip() for value in [street, number] if value)

    parts = [
        street_line,
        address_data.get("neighborhood"),
        address_data.get("city"),
        address_data.get("state"),
        "Brasil",
    ]

    return " ".join(str(part).strip() for part in parts if part)


def geocode_address(address_data: dict[str, Any]) -> Coordinates | GeocodingError:
    query = build_address_query(address_data)

    try:
        response = requests.get(
            NOMINATIM_SEARCH_URL,
            params={
                "q": query,
                "format": "json",
                "polygon": 1,
                "addressdetails": 1,
                "limit": 1,
            },
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException:
        return GeocodingError("Failed to geocode address.")

    try:
        results = response.json()
    except ValueError:
        return GeocodingError("Geocoding response was not valid JSON.")

    if not results:
        return GeocodingError("Address could not be geocoded.")

    first_result = results[0]

    try:
        latitude = Decimal(str(first_result["lat"])).quantize(COORDINATE_PRECISION)
        longitude = Decimal(str(first_result["lon"])).quantize(COORDINATE_PRECISION)
        return Coordinates(latitude=latitude, longitude=longitude)
    except (KeyError, InvalidOperation):
        return GeocodingError("Geocoding response did not include valid coordinates.")
