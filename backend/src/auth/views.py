from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.permission import IsAuthenticated, IsNotAuthenticated
from backend.src.auth.schemas import LoginData
from backend.src.auth.security import generate_jwt_token, verify_password
from backend.src.config import settings
from backend.src.database.dependencies import get_db
from backend.src.permissions.dependencies import PermissionsDependency
from backend.src.users import services as user_service
from backend.src.users.schemas import UserSchema

router = APIRouter()


@router.post(
    "/login",
    response_model=UserSchema,
    dependencies=[Depends(PermissionsDependency([IsNotAuthenticated]))],
)
async def login(
    user_data: LoginData, response: Response, db_session: AsyncSession = Depends(get_db)
) -> Any:
    """Log in user."""
    user = await user_service.get_by_email(db_session=db_session, email=user_data.email)
    if user and user.is_active and verify_password(user_data.password, user.password):
        response.set_cookie(
            "Authorization",
            value=f"Bearer {generate_jwt_token({'user_id': user.id})}",
            httponly=True,
            max_age=settings.JWT_AUTH_TOKEN_EXPIRY,
            secure=settings.DOMAIN_HTTPS,
        )
        return user

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
    )


@router.post("/logout", dependencies=[Depends(PermissionsDependency([IsAuthenticated]))])
async def logout(response: Response) -> Any:
    """Log out user."""
    response.set_cookie("Authorization", max_age=0)
    return {"success": True}
