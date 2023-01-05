from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.dashboard import services as dashboard_services
from backend.src.dashboard.models import Dashboard
from backend.src.database.dependencies import get_db
from backend.src.users.dependencies import get_current_user
from backend.src.users.models import User


async def get_current_user_dashboard(
    db_session: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
) -> Dashboard:
    if dashboard := await dashboard_services.get_by_user_id(db_session=db_session, user_id=user.id):
        return dashboard
    raise HTTPException(status_code=404, detail="Dashboard for current user doesn't found.")
