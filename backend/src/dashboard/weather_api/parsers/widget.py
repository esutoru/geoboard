from ...constants import WidgetType
from ...models import Widget
from ..client.exceptions import WeatherApiException
from ..client.types import WeatherApiForecast
from ..types import ForecastWidget


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
    match widget_type:
        case WidgetType.uv_index:
            return {"uv_index": data["current"]["uv"]}
        case WidgetType.wind_status:
            return {"speed": data["current"]["wind_kph"]}
    return None
