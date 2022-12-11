from abc import ABC, abstractmethod
from typing import Type

from fastapi import Depends, HTTPException, Request, status

from backend.src.users.dependencies import get_current_user
from backend.src.users.models import User


class BasePermission(ABC):
    """
    Abstract permission that all other Permissions must be inherited from.
    Defines basic error message, status & error codes.
    Upon initialization, calls abstract method  `has_required_permissions`
    which will be specific to concrete implementation of Permission class.
    You would write your permissions like this:
    .. code-block:: python
        class TeapotUserAgentPermission(BasePermission):
            def has_required_permissions(self, request: Request) -> bool:
                return request.headers.get('User-Agent') == "Teapot v1.0"
    """

    error_msg = [{"msg": "You don't have permission to access or modify this resource."}]
    status_code = status.HTTP_403_FORBIDDEN

    @abstractmethod
    def has_required_permissions(self) -> bool:
        ...

    def __init__(self, request: Request, user: User) -> None:
        self.user = user
        self.request = request

        if not self.has_required_permissions():
            raise HTTPException(status_code=self.status_code, detail=self.error_msg)


class AllowAny(BasePermission):
    """
    Allow any access.
    This isn't strictly required, since you could use an empty
    permission_classes list, but it's useful because it makes the intention
    more explicit.
    """

    def has_required_permissions(self) -> bool:
        return True


class PermissionsDependency:
    """
    Permission dependency that is used to define and check all the permission
    classes from one place inside route definition.
    Use it as an argument to FastAPI's `Depends` as follows:
    .. code-block:: python
        app = FastAPI()
        @app.get(
            "/teapot/",
            dependencies=[Depends(
                PermissionsDependency([TeapotUserAgentPermission]))]
        )
        async def teapot() -> dict:
            return {"teapot": True}
    """

    def __init__(self, permissions_classes: list[Type[BasePermission]]) -> None:
        self.permissions_classes = permissions_classes

    def __call__(self, request: Request, user: User = Depends(get_current_user)) -> None:
        for permission_class in self.permissions_classes:
            permission_class(request=request, user=user)
