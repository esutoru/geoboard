from typing import Any

from fastapi import APIRouter, Depends

from backend.src.users.dependencies import get_current_user
from backend.src.users.models import User
from backend.src.users.schemas import UserSchema

router = APIRouter()


@router.get("/me", response_model=UserSchema)
async def get_me(user: User = Depends(get_current_user)) -> Any:
    return user
