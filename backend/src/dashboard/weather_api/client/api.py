from types import TracebackType
from typing import Any, Callable, Type
from urllib.parse import urljoin

from aiohttp import ClientError, ClientSession

from .exceptions import WeatherApiException


def session_exception_handler(func: Callable) -> Callable:
    async def wrapper(*args: Any, **kwargs: Any) -> Callable:
        try:
            return await func(*args, **kwargs)
        except ClientError:
            raise WeatherApiException()

    return wrapper


class Response:
    def __init__(self, data: Any, status: int, ok: bool):
        self.data = data
        self.status = status
        self.ok = ok


class HttpClient:
    def __init__(self, url: str, key: str, session: ClientSession | None = None) -> None:
        self._url = url
        self._key = key

        if session is None:
            session = ClientSession()
        self._session = session

    async def __aenter__(self) -> "HttpClient":
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._session.close()

    @session_exception_handler
    async def get(self, path: str, *, params: dict[str, str]) -> Response:
        context_manager = self._session.get(
            url=self._prepare_url(path), params=self._prepare_params(params)
        )
        async with context_manager as response:
            return Response(await response.json(), response.status, response.ok)

    async def close(self) -> None:
        await self._session.close()

    def _prepare_url(self, path: str) -> str:
        return urljoin(self._url, path)

    def _prepare_params(self, params: dict[str, str]) -> dict[str, str]:
        return {**params, "key": self._key}
