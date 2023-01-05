from .client.types import WeatherApiLocation
from .types import Location


def parse_location(data: WeatherApiLocation) -> Location:
    return {
        "name": data["name"],
        "region": data["region"],
        "country": data["country"],
        "code": data["url"],
    }
