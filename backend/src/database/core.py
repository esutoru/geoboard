from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from backend.src.config import settings
from backend.src.database.utils import resolve_table_name

url_object = URL.create(
    "postgresql+asyncpg",
    username=settings.DATABASE_USER,
    password=settings.DATABASE_PASSWORD,
    host=settings.DATABASE_HOST,
    port=settings.DATABASE_PORT,
    database=settings.DATABASE_NAME,
)

engine = create_async_engine(url_object, future=True, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return resolve_table_name(self.__name__)
