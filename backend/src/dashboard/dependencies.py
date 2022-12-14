from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.dashboard import services as dashboard_services
from backend.src.dashboard.models import Dashboard, Widget
from backend.src.database.dependencies import get_db
from backend.src.users.dependencies import get_current_user
from backend.src.users.models import User


async def get_dashboard(
    db_session: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
) -> Dashboard:
    if dashboard := await dashboard_services.get_by_user_id(db_session=db_session, user_id=user.id):
        return dashboard
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard for current user doesn't found."
    )


async def get_widget(db_session: AsyncSession = Depends(get_db), uuid: UUID = Path(...)) -> Widget:
    if widget := await dashboard_services.get_widget_by_uuid(db_session=db_session, uuid=uuid):
        return widget
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Widget with uuid {uuid} doesn't found."
    )
