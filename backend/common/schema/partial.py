from typing import Any, Optional, Type

from pydantic import BaseModel


def convert_to_optional(schema: Type[BaseModel]) -> dict[str, Any]:
    """
    Use with inheritor of scheme to make it partial.

    Example:

    class OriginalSchema(BaseModel):
        email: EmailStr
        first_name: str

    class PartialSchema(OriginalSchema):
        __annotations__ = convert_to_optional(OriginalSchema)

    This will be identical to the following schema:

    class PartialSchema(BaseModel):
        email: EmailStr | None
        first_name: str | None
    """

    return {k: Optional[v] for k, v in schema.__annotations__.items()}
