from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from backend.src.dashboard.constants import TemperatureScale
from backend.src.database.core import Base

if TYPE_CHECKING:
    from backend.src.users.models import User


class Dashboard(Base):
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)

    location: Mapped[str] = Column(String, nullable=False)
    temperature_scale: Mapped[str] = Column(
        String, default=TemperatureScale.celsius, nullable=False
    )

    user_id: Mapped[int] = Column(Integer, ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="dashboard")

    widgets: Mapped[list["Widget"]] = relationship("Widget", back_populates="dashboard")


class Widget(Base):
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)

    dashboard_id: Mapped[int] = Column(Integer, ForeignKey("dashboard.id"))
    dashboard: Mapped["Dashboard"] = relationship("Dashboard", back_populates="widgets")

    widget_type: Mapped[str] = Column(String, nullable=False)

    x: Mapped[int] = Column(Integer, nullable=False)
    y: Mapped[int] = Column(Integer, nullable=False)

    width: Mapped[int] = Column(Integer, nullable=False)
    height: Mapped[int] = Column(Integer, nullable=False)
