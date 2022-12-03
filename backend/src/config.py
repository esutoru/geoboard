from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    DOMAIN_HTTPS: bool

    JWT_AUTH_ALGORITHM: str
    JWT_AUTH_SECRET_KEY: str
    JWT_AUTH_TOKEN_EXPIRY: int = 14 * 24 * 60 * 60

    SQLALCHEMY_DATABASE_URI: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
