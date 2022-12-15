from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    DEBUG: bool = False
    DOMAIN_HTTPS: bool

    JWT_AUTH_ALGORITHM: str
    JWT_AUTH_SECRET_KEY: str
    JWT_AUTH_TOKEN_EXPIRY: int = 14 * 24 * 60 * 60

    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
