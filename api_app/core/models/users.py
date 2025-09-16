import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String, CHAR, DateTime, Integer, BigInteger

from api_app.core.config import settings
from api_app.core.models.base import Base


class TicketAction:
    REFERRAL = 'rfrl'
    BUYER = 'buyr'

    DISPLAY_NAMES = {
        REFERRAL: 'Приглашение',
        BUYER: 'Покупка',
    }

    ALL_STATUS = [
        REFERRAL,
        BUYER,
    ]

    @classmethod
    def get_display_name(cls, ticked_action):
        return cls.DISPLAY_NAMES.get(ticked_action, 'Неизвестно')


class User(Base):
    __tablename__ = "users"

    entrant_id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True
    )
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[str | None] = mapped_column(String(50))
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))
    phone_number: Mapped[str | None] = mapped_column(String(12))
    language_code: Mapped[str | None] = mapped_column(
        String(2), default=settings.default_language_code
    )
    user_uuid: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    last_activity: Mapped[datetime | None] = mapped_column(DateTime)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="Ticket.user_id",
    )
    initiated_tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket", back_populates="initiator", foreign_keys="Ticket.initiator_id"
    )


class Prize(Base):
    __tablename__ = "prizes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(default=False)
    weight: Mapped[int] = mapped_column(default=1)
    description: Mapped[str] = mapped_column(String(255), default="")
    quantity: Mapped[int] = mapped_column(default=0)
    check_quantity: Mapped[bool] = mapped_column(default=False)
    tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket", back_populates="prize", foreign_keys="Ticket.prize_id"
    )


class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    action: Mapped[str | None] = mapped_column(CHAR(4))
    action_description: Mapped[str] = mapped_column(String(255), default="")
    is_fired: Mapped[bool] = mapped_column(default=False)
    fired_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), index=True)
    user: Mapped["User"] = relationship(
        "User", back_populates="tickets", foreign_keys=[user_id]
    )

    initiator_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id"), index=True
    )
    initiator: Mapped["User"] = relationship(
        "User", back_populates="initiated_tickets", foreign_keys=[initiator_id]
    )

    prize_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("prizes.id"))
    prize: Mapped["Prize|None"] = relationship(
        "Prize", back_populates="tickets", foreign_keys=[prize_id]
    )
