from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, DateTime

from api_app.core.models.base import Base


class RequiredChannel(Base):
    __tablename__ = "required_channels"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    name: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)
