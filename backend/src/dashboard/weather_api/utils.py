from typing import Any

from backend.src.config import settings

from .client.client import WeatherApiClient
from .parsers import parse_location


def get_client() -> WeatherApiClient:
    return WeatherApiClient(url=settings.WEATHER_API_URL, key=settings.WEATHER_API_KEY)


async def search_location(query: str) -> Any:
    """Returns matching cities and towns as an array."""
    async with get_client() as client:
        return [parse_location(location) for location in await client.search_location(query)]
