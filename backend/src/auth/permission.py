from fastapi import status

from backend.src.permissions.dependencies import BasePermission


class IsAuthenticated(BasePermission):
    """Allows access only to authenticated users."""

    status_code = status.HTTP_401_UNAUTHORIZED

    def has_required_permissions(self) -> bool:
        return bool(self.user and self.user.is_active)


class IsNotAuthenticated(BasePermission):
    """Allows access only to authenticated users."""

    def has_required_permissions(self) -> bool:
        return bool(not self.user)
