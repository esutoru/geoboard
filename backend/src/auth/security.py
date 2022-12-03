from datetime import datetime, timedelta

from jose import jwt
from jose.exceptions import JWKError, JWTError
from passlib.context import CryptContext

from backend.src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_jwt_token(params: dict) -> str:
    exp = datetime.utcnow() + timedelta(seconds=settings.JWT_AUTH_TOKEN_EXPIRY)
    return jwt.encode(
        {**params, "exp": exp}, settings.JWT_AUTH_SECRET_KEY, algorithm=settings.JWT_AUTH_ALGORITHM
    )


def get_jwt_token_params(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.JWT_AUTH_SECRET_KEY)
    except (JWKError, JWTError):
        return None


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
