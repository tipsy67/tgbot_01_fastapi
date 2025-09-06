from datetime import datetime, timezone

from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String, CHAR, DateTime, Integer

from api_app.core.config import settings


class TicketAction:
    REFERRAL = 'rfrl'
    BUYER = 'buyr'

    DISPLAY_NAMES = {
        REFERRAL: 'Приглашение',
        BUYER: 'Покупка',
    }

    ALL_STATUS = [REFERRAL, BUYER,]

    @classmethod
    def get_display_name(cls, ticked_action):
        return cls.DISPLAY_NAMES.get(ticked_action, 'Неизвестно')

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
    tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="Ticket.user_id"
    )
    initiated_tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket",
        back_populates="initiator",
        foreign_keys="Ticket.initiator_id"
    )


class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    action: Mapped[CHAR] = mapped_column(CHAR(4))
    action_description: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    initiator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="tickets", foreign_keys=[user_id])
    initiator: Mapped["User"] = relationship("User", back_populates="initiated_tickets", foreign_keys=[initiator_id])

    is_fired: Mapped[bool] = mapped_column(default=False)
    fired_at: Mapped[datetime] = mapped_column(DateTime)
    prize_id: Mapped[int] = mapped_column(Integer, ForeignKey("prizes.id"), nullable=False)
    ticket = relationship(
        "Prize",
        back_populates="prizes"
    )

class Prize(Base):
    __tablename__ = "prizes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(default=False)
    description: Mapped[str] = mapped_column(String(255), default="")
    tickets = relationship(
        "Ticket",
        back_populates="tickets",
    )
