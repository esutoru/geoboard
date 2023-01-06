from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.permission import IsAuthenticated
from backend.src.permissions.dependencies import PermissionsDependency

from ..database.dependencies import get_db
from . import services as dashboard_services
from . import weather_api
from .dependencies import get_current_user_dashboard
from .exceptions import WeatherApiHttpException
from .models import Dashboard
from .schemas import (
    DashboardSchema,
    ExternalServiceNotAvailable,
    LocationSchema,
    SearchLocationIn,
    WidgetIn,
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
    # response_model=DashboardSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
)
async def dashboard(user_dashboard: Dashboard = Depends(get_current_user_dashboard)) -> Any:
    """Returns weather data for current dashboard settings."""

    try:
        return await weather_api.get_location_forecast(
            user_dashboard.location, user_dashboard.temperature_scale, user_dashboard.widgets
        )
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


@router.post(
    "/widget",
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
)
async def add_widget(
    data: WidgetIn,
    db_session: AsyncSession = Depends(get_db),
    user_dashboard: Dashboard = Depends(get_current_user_dashboard),
) -> Any:
    """Add new widget."""

    widget = await dashboard_services.create_widget(
        db_session=db_session, dashboard_id=user_dashboard.id, data=data
    )

    return {"uuid": widget.uuid}
