from typing import Any

from fastapi import APIRouter, Depends

from backend.src.auth.permission import IsAuthenticated
from backend.src.permissions.dependencies import PermissionsDependency

from . import weather_api
from .dependencies import get_current_user_dashboard
from .exceptions import WeatherApiHttpException
from .models import Dashboard
from .schemas import (
    DashboardSchema,
    ExternalServiceNotAvailable,
    LocationSchema,
    SearchLocationIn,
)
from .weather_api.client.exceptions import WeatherApiException

router = APIRouter(
    responses={
        400: {
            "model": ExternalServiceNotAvailable,
            "description": "External service is not available",
        }
    }
)


@router.get(
    "/",
    response_model=DashboardSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
)
async def dashboard(data: Dashboard = Depends(get_current_user_dashboard)) -> Any:
    """Returns weather data for current dashboard settings."""
    try:
        return {
            "temperature_scale": data.temperature_scale.name,
            **(await weather_api.get_location_forecast(data.location)),
        }
    except WeatherApiException:
        raise WeatherApiHttpException()


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
