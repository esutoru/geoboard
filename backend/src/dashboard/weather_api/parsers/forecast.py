import calendar
from datetime import datetime

from dateutil.parser import ParserError
from dateutil.parser import parse as parse_date

from ...models import Widget
from ..client.exceptions import WeatherApiException
from ..client.types import WeatherApiForecast
from ..types import (
    DayForecast,
    Forecast,
    ForecastCondition,
    ForecastLocation,
    ForecastTemperature,
)
from .widget import parse_widget


def parse_forecast(
    data: WeatherApiForecast, temperature_scale: str, widgets: list[Widget]
) -> Forecast:
    return {
        "temperature_scale": temperature_scale,
        "location": _parse_forecast_location(data),
        "temperature": _parse_forecast_temperature(data),
        "condition": _parse_forecast_condition(data),
        "forecast": _parse_forecast(data),
        "widgets": [parse_widget(data, widget) for widget in widgets],
    }


def _parse_forecast_location(data: WeatherApiForecast) -> ForecastLocation:
    local_time = _parse_date(data["location"]["localtime"])

    return {
        "name": data["location"]["name"],
        "region": data["location"]["region"],
        "country": data["location"]["country"],
        "date": local_time.strftime("%Y-%m-%d"),
        "time": local_time.strftime("%H:%M"),
        "day_of_week": calendar.day_name[local_time.weekday()],
    }


def _parse_forecast_temperature(data: WeatherApiForecast) -> ForecastTemperature:
    return {"celsius": data["current"]["temp_c"], "fahrenheit": data["current"]["temp_f"]}


def _parse_forecast_condition(data: WeatherApiForecast) -> ForecastCondition:
    return {
        "status": data["current"]["condition"]["text"],
        "icon": data["current"]["condition"]["icon"],
    }


def _parse_forecast(data: WeatherApiForecast) -> list[DayForecast]:
    return [
        {
            "date": day_forecast["date"],
            "day_of_week": calendar.day_name[_parse_date(day_forecast["date"]).weekday()],
            "condition": {
                "status": day_forecast["day"]["condition"]["text"],
                "icon": day_forecast["day"]["condition"]["icon"],
            },
            "temperature": {
                "max": {
                    "celsius": day_forecast["day"]["maxtemp_c"],
                    "fahrenheit": day_forecast["day"]["maxtemp_f"],
                },
                "min": {
                    "celsius": day_forecast["day"]["maxtemp_c"],
                    "fahrenheit": day_forecast["day"]["maxtemp_f"],
                },
            },
        }
        for day_forecast in data["forecast"]["forecastday"][1:]
    ]


def _parse_date(value: str) -> datetime:
    try:
        return parse_date(value)
    except ParserError:
        raise WeatherApiException()
