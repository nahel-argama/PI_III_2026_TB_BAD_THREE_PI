import time
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


def build_address_queries(address_data: dict[str, Any]) -> list[str]:
    street = address_data.get("street")
    number = address_data.get("number")
    neighborhood = address_data.get("neighborhood")
    city = address_data.get("city")
    state = address_data.get("state")
    country = "Brasil"

    queries = []

    def format_query(parts):
        return ", ".join(str(p).strip() for p in parts if p)

    # 1. Full address (Street + Number, Neighborhood, City, State, Country)
    if street:
        street_part = f"{street} {number}".strip() if number else street
        queries.append(format_query([street_part, neighborhood, city, state, country]))

    # 2. Neighborhood, City, State, Country
    if neighborhood:
        queries.append(format_query([neighborhood, city, state, country]))

    # 3. City, State, Country
    if city:
        queries.append(format_query([city, state, country]))

    # 4. State, Country
    if state:
        queries.append(format_query([state, country]))

    # Remove duplicates while preserving order
    seen = set()
    unique_queries = []
    for q in queries:
        if q not in seen:
            seen.add(q)
            unique_queries.append(q)

    return unique_queries


def geocode_address(address_data: dict[str, Any]) -> Coordinates | GeocodingError:
    queries = build_address_queries(address_data)

    last_error = GeocodingError("Address could not be geocoded.")

    for idx, query in enumerate(queries):
        if idx > 0:
            time.sleep(1.1)  # Respect Nominatim's 1 request per second limit

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
            last_error = GeocodingError("Failed to geocode address.")
            continue

        try:
            results = response.json()
        except ValueError:
            last_error = GeocodingError("Geocoding response was not valid JSON.")
            continue

        if not isinstance(results, list) or not results:
            last_error = GeocodingError("Address could not be geocoded.")
            continue

        first_result = results[0]
        if not isinstance(first_result, dict):
            last_error = GeocodingError("Geocoding response did not include valid coordinates.")
            continue

        try:
            latitude = Decimal(str(first_result["lat"])).quantize(COORDINATE_PRECISION)
            longitude = Decimal(str(first_result["lon"])).quantize(COORDINATE_PRECISION)
            return Coordinates(latitude=latitude, longitude=longitude)
        except (KeyError, InvalidOperation, TypeError):
            last_error = GeocodingError("Geocoding response did not include valid coordinates.")
            continue

    return last_error
