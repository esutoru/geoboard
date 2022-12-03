from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime


class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def _updated_at(mapper: Any, connection: Any, target: Any) -> None:
        target.updated_at = datetime.utcnow()
