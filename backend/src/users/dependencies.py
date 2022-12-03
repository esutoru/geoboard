from fastapi import Depends, Request
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.security import get_jwt_token_params
from backend.src.database.dependencies import get_db
from backend.src.users import services as user_service
from backend.src.users.models import User


async def get_current_user(
    request: Request, db_session: AsyncSession = Depends(get_db)
) -> User | None:
    authorization_header_value = request.cookies.get("Authorization")
    if not authorization_header_value:
        return None

    scheme, token = get_authorization_scheme_param(authorization_header_value)
    if not token or scheme.lower() != "bearer":
        return None

    if params := get_jwt_token_params(token):
        return await user_service.get(db_session=db_session, user_id=params["user_id"])

    return None
