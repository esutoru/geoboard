from types import TracebackType
from typing import Optional, Type

from aiohttp import ClientSession

from .api import HttpClient
from .exceptions import WeatherApiException
from .types import WeatherApiLocation


class WeatherApiClient:
    def __init__(self, url: str, key: str, session: ClientSession | None = None) -> None:
        self._http_client = HttpClient(url, key, session)

    async def __aenter__(self) -> "WeatherApiClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self._http_client.close()

    async def search_location(self, query: str) -> list[WeatherApiLocation]:
        """Returns matching cities and towns as an array."""
        response = await self._http_client.get("search.json", params={"q": query})
        if response.ok:
            return response.data
        raise WeatherApiException()

    async def close(self) -> None:
        await self._http_client.close()
