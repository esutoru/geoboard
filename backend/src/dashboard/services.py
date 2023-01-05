from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.config import settings
from backend.src.dashboard.models import Dashboard


async def create(*, db_session: AsyncSession, user_id: int) -> Dashboard | None:
    """Create new user instance in db."""
    dashboard = Dashboard(location=settings.DEFAULT_DASHBOARD_LOCATION, user_id=user_id)
    db_session.add(dashboard)
    await db_session.commit()
    await db_session.refresh(dashboard)
    return dashboard
