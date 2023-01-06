from pydantic import BaseModel, EmailStr

from backend.common.schema.partial import convert_to_optional


class UserSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool

    class Config:
        orm_mode = True


class UserRegistrationSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    is_active: bool

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserPartialUpdateSchema(UserUpdateSchema):
    __annotations__ = convert_to_optional(UserUpdateSchema)
