from functools import wraps
from typing import Callable

import anyio


def async_to_sync(function: Callable) -> Callable:
    """Run async function in synced function."""

    @wraps(function)
    def wrapper(*args: object, **kwargs: object) -> object:
        async def async_function_wrapper() -> Callable:
            return await function(*args, **kwargs)

        return anyio.run(async_function_wrapper)

    return wrapper
