from fastapi import APIRouter

from backend.src.auth.views import router as auth_router
from backend.src.dashboard.views import router as dashboard_router
from backend.src.users.views import router as users_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
