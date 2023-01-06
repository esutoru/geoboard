from backend.src.config import settings

from ..models import Widget
from .client.client import WeatherApiClient
from .parsers import parse_forecast, parse_location, parse_widget
from .types import Forecast, ForecastWidget, Location


def get_client() -> WeatherApiClient:
    return WeatherApiClient(url=settings.WEATHER_API_URL, key=settings.WEATHER_API_KEY)


async def search_location(query: str) -> list[Location]:
    """Returns matching cities and towns as an array."""
    async with get_client() as client:
        return [parse_location(location) for location in await client.search_location(query)]


async def get_location_forecast(
    location: str, temperature_scale: str, widgets: list[Widget]
) -> Forecast:
    async with get_client() as client:
        return parse_forecast(
            await client.get_location_forecast(location, days=8), temperature_scale, widgets
        )


async def get_widget_data(location: str, widget: Widget) -> ForecastWidget:
    async with get_client() as client:
        return parse_widget((await client.get_location_forecast(location, days=1)), widget)
