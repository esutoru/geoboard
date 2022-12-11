from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.permission import IsAuthenticated
from backend.src.database.dependencies import get_db
from backend.src.permissions.dependencies import PermissionsDependency
from backend.src.users import services as user_service
from backend.src.users.dependencies import get_current_user
from backend.src.users.models import User
from backend.src.users.schemas import (
    UserPartialUpdateSchema,
    UserSchema,
    UserUpdateSchema,
)

router = APIRouter()


@router.get(
    "/me",
    response_model=UserSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
)
async def get_me(user: User = Depends(get_current_user)) -> Any:
    """Get current user data."""
    return user


@router.put(
    "/me",
    response_model=UserSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
)
async def update_me(
    data: UserUpdateSchema,
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
) -> Any:
    """Update current user data."""
    return await user_service.update(db_session=db_session, user=user, data=data)


@router.patch(
    "/me",
    response_model=UserSchema,
    dependencies=[Depends(PermissionsDependency([IsAuthenticated]))],
)
async def update_me_partial(
    data: UserPartialUpdateSchema,
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
) -> Any:
    """Partial update current user data."""
    return await user_service.update(db_session=db_session, user=user, data=data)
