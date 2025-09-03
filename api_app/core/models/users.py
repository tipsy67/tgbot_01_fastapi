from datetime import datetime

from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from api_app.core.config import settings


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(50))
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    phone_number: Mapped[Optional[str]] = mapped_column(String(12))
    language_code: Mapped[Optional[str]] = mapped_column(String(2), default= settings.default_language_code)
    token: Mapped[Optional[str] ] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column()
    last_activity: Mapped[datetime] = mapped_column()
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    ticket_id: Mapped[Optional[str]] = mapped_column()


class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_fired: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column()
    action: Mapped[Optional[str]] = mapped_column(default=None)
