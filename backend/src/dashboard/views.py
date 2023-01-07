from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.permission import IsAuthenticated
from backend.src.permissions.dependencies import PermissionsDependency

from ..database.dependencies import get_db
from . import services as dashboard_services
from . import weather_api
from .dependencies import get_dashboard, get_widget
from .exceptions import WeatherApiHttpException
from .models import Dashboard, Widget
from .schemas import (
    DashboardSchema,
    ExternalServiceNotAvailable,
    LocationSchema,
    SearchLocationIn,
    WidgetCreateSchema,
    WidgetDoesNotFound,
    WidgetPartialUpdateSchema,
    WidgetSchema,
    WidgetUpdateSchema,
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
async def dashboard_detail(dashboard: Dashboard = Depends(get_dashboard)) -> Any:
    """Returns weather data for current dashboard settings."""

    try:
        return await weather_api.get_location_forecast(
            dashboard.location, dashboard.temperature_scale, dashboard.widgets
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
    response_model=WidgetSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
)
async def add_widget(
    data: WidgetCreateSchema,
    db_session: AsyncSession = Depends(get_db),
    dashboard: Dashboard = Depends(get_dashboard),
) -> Any:
    """Add new widget."""

    location = dashboard.location
    widget = await dashboard_services.create_widget(
        db_session=db_session, dashboard_id=dashboard.id, data=data
    )

    return await weather_api.get_widget_data(location, widget)


@router.put(
    "/widget/{uuid}",
    response_model=WidgetSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
)
async def update_widget(
    data: WidgetUpdateSchema,
    db_session: AsyncSession = Depends(get_db),
    widget: Widget = Depends(get_widget),
    dashboard: Dashboard = Depends(get_dashboard),
) -> Any:
    """Update existed widget."""
    location = dashboard.location
    updated_widget = await dashboard_services.update_widget(
        db_session=db_session, widget=widget, data=data
    )
    return await weather_api.get_widget_data(location, updated_widget)


@router.patch(
    "/widget/{uuid}",
    response_model=WidgetSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
)
async def update_widget_partial(
    data: WidgetPartialUpdateSchema,
    db_session: AsyncSession = Depends(get_db),
    widget: Widget = Depends(get_widget),
    dashboard: Dashboard = Depends(get_dashboard),
) -> Any:
    """Partial update existed widget."""
    location = dashboard.location
    updated_widget = await dashboard_services.update_widget(
        db_session=db_session, widget=widget, data=data
    )
    return await weather_api.get_widget_data(location, updated_widget)


@router.delete(
    "/widget/{uuid}",
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": WidgetDoesNotFound, "description": "Widget doesn't found."}},
)
async def delete_widget(
    db_session: AsyncSession = Depends(get_db), widget: Widget = Depends(get_widget)
) -> None:
    """Delete existed widget."""
    await dashboard_services.delete_widget_by_uuid(db_session=db_session, uuid=widget.uuid)
