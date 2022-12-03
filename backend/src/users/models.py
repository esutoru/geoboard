from sqlalchemy import Boolean, Column, Integer, String

from backend.src.database.core import Base
from backend.src.database.mixins import TimeStampMixin


class User(Base, TimeStampMixin):
    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, index=True)
    password: str = Column(String, nullable=False)

    is_active: bool = Column(Boolean, default=True)
