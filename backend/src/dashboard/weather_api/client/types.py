from typing import TypedDict


class WeatherApiLocation(TypedDict):
    name: str
    region: str
    country: str
    url: str
