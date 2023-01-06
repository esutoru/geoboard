from typing import TypedDict


class WeatherApiLocation(TypedDict):
    name: str
    region: str
    country: str
    url: str


class WeatherApiForecastLocation(TypedDict):
    name: str
    region: str
    country: str
    localtime: str


class WeatherApiForecastCurrentCondition(TypedDict):
    text: str
    icon: str


class WeatherApiForecastCurrent(TypedDict):
    temp_c: float
    temp_f: int
    condition: WeatherApiForecastCurrentCondition
    uv: float
    wind_kph: float
    humidity: int
    vis_km: float


class WeatherApiForecastForecastForecastDayDay(TypedDict):
    maxtemp_c: float
    maxtemp_f: float
    mintemp_c: float
    mintemp_f: float
    condition: WeatherApiForecastCurrentCondition


class WeatherApiForecastForecastForecastDayAstro(TypedDict):
    sunrise: str
    sunset: str


class WeatherApiForecastForecastForecastDay(TypedDict):
    date: str
    day: WeatherApiForecastForecastForecastDayDay
    astro: WeatherApiForecastForecastForecastDayAstro


class WeatherApiForecastForecast(TypedDict):
    forecastday: list[WeatherApiForecastForecastForecastDay]


class WeatherApiForecast(TypedDict):
    location: WeatherApiForecastLocation
    current: WeatherApiForecastCurrent
    forecast: WeatherApiForecastForecast
