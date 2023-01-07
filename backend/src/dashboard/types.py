from typing import Literal

TemperatureScales = Literal["celsius", "fahrenheit"]

WidgetTypes = Literal[
    "uv_index", "wind_status", "sunrise_sunset", "humidity", "visibility", "min_max_temperature"
]
