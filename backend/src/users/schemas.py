from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True


class UserRegistrationSchema(BaseModel):
    email: EmailStr
    password: str
    is_active: bool

    class Config:
        orm_mode = True
