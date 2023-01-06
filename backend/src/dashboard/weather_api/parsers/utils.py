from datetime import datetime

from dateutil.parser import ParserError, parse

from ..client.exceptions import WeatherApiException


def parse_date(value: str) -> datetime:
    try:
        return parse(value)
    except ParserError:
        raise WeatherApiException()
