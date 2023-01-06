from typing import TypedDict
from uuid import UUID


class Location(TypedDict):
    name: str
    region: str
    country: str
    code: str


class ForecastLocation(TypedDict):
    name: str
    region: str
    country: str
    date: str
    time: str
    day_of_week: str


class ForecastTemperature(TypedDict):
    celsius: float
    fahrenheit: float


class ForecastCondition(TypedDict):
    status: str
    icon: str


class DayForecastTemperature(TypedDict):
    max: ForecastTemperature
    min: ForecastTemperature


class DayForecast(TypedDict):
    date: str
    day_of_week: str
    temperature: DayForecastTemperature
    condition: ForecastCondition


class ForecastWidget(TypedDict):
    uuid: UUID
    widget_type: str

    x: int
    y: int

    width: int
    height: int

    data: dict


class Forecast(TypedDict):
    temperature_scale: str
    location: ForecastLocation
    temperature: ForecastTemperature
    condition: ForecastCondition
    forecast: list[DayForecast]
    widgets: list[ForecastWidget]
