from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.config import settings
from backend.src.dashboard.models import Dashboard, Widget
from backend.src.dashboard.schemas import WidgetIn


async def get_by_user_id(*, db_session: AsyncSession, user_id: int) -> Dashboard | None:
    """Returns a dashboard object based on user id."""
    result = await db_session.execute(select(Dashboard).filter(Dashboard.user_id == user_id))
    return result.scalars().one_or_none()


async def create(*, db_session: AsyncSession, user_id: int) -> Dashboard:
    """Create new dashboard instance in db."""
    dashboard = Dashboard(location=settings.DEFAULT_DASHBOARD_LOCATION, user_id=user_id)
    db_session.add(dashboard)
    await db_session.commit()
    await db_session.refresh(dashboard)
    return dashboard


async def create_widget(*, db_session: AsyncSession, dashboard_id: int, data: WidgetIn) -> Widget:
    """Create new user widget instance in db."""

    widget = Widget(
        dashboard_id=dashboard_id,
        widget_type=data.widget_type,
        x=data.x,
        y=data.y,
        width=data.width,
        height=data.height,
    )

    db_session.add(widget)
    await db_session.commit()
    await db_session.refresh(widget)
    return widget
