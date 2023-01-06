from ...constants import WidgetType
from ...models import Widget
from ..client.exceptions import WeatherApiException
from ..client.types import WeatherApiForecast
from ..types import ForecastWidget
from .utils import parse_date


def parse_widget(data: WeatherApiForecast, widget: Widget) -> ForecastWidget:
    widget_data = _parse_data(data, widget.widget_type)
    if widget_data is None:
        raise WeatherApiException()

    return {
        "uuid": widget.uuid,
        "widget_type": widget.widget_type,
        "x": widget.x,
        "y": widget.y,
        "width": widget.width,
        "height": widget.height,
        "data": widget_data,
    }


def _parse_data(data: WeatherApiForecast, widget_type: str) -> dict | None:
    day_forecast = data["forecast"]["forecastday"][0]
    match widget_type:
        case WidgetType.uv_index:
            return {"uv_index": data["current"]["uv"]}
        case WidgetType.wind_status:
            return {"speed": data["current"]["wind_kph"]}
        case WidgetType.sunrise_sunset:
            return {
                "sunrise": parse_date(day_forecast["astro"]["sunrise"]).strftime("%H:%M"),
                "sunset": parse_date(day_forecast["astro"]["sunset"]).strftime("%H:%M"),
            }
        case WidgetType.humidity:
            return {"value": data["current"]["humidity"]}
        case WidgetType.visibility:
            return {"value": data["current"]["vis_km"]}
        case WidgetType.min_max_temperature:
            return {
                "min": {
                    "celsius": day_forecast["day"]["mintemp_c"],
                    "fahrenheit": day_forecast["day"]["mintemp_f"],
                },
                "max": {
                    "celsius": day_forecast["day"]["maxtemp_c"],
                    "fahrenheit": day_forecast["day"]["maxtemp_f"],
                },
            }
    return None
