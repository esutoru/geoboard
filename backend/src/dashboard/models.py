import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from backend.src.database.core import Base

if TYPE_CHECKING:
    from backend.src.users.models import User


class TemperatureScale(enum.Enum):
    celsius = "celsius"
    fahrenheit = "fahrenheit"


class Dashboard(Base):
    id: int = Column(Integer, primary_key=True, index=True)

    location: str = Column(String, nullable=False)
    temperature_scale: TemperatureScale = Column(
        Enum(TemperatureScale), default=TemperatureScale.celsius, nullable=False
    )

    user_id: Mapped[int] = Column(Integer, ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="dashboard")
