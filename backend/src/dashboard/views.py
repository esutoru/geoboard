from typing import Any

from fastapi import APIRouter, Depends

from backend.src.auth.permission import IsAuthenticated
from backend.src.permissions.dependencies import PermissionsDependency

from . import weather_api
from .exceptions import WeatherApiHttpException
from .schemas import ExternalServiceNotAvailable, LocationSchema, SearchLocationIn
from .weather_api.client.exceptions import WeatherApiException

router = APIRouter(
    responses={
        400: {
            "model": ExternalServiceNotAvailable,
            "description": "External service is not available",
        }
    }
)


@router.post(
    "/search-location",
    response_model=list[LocationSchema],
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
)
async def search_location(data: SearchLocationIn) -> Any:
    """Returns matching cities and towns as an array."""
    try:
        return await weather_api.search_location(data.query)
    except WeatherApiException:
        raise WeatherApiHttpException()
