from pydantic import BaseModel, EmailStr, validator


class LoginData(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_required(cls, value: str) -> str:
        if not value:
            raise ValueError("Must not be empty string")
        return value

    class Config:
        orm_mode = True
