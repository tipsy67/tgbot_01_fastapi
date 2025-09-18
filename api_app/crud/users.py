import logging
import uuid

from datetime import datetime
from datetime import timezone

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import case
from sqlalchemy.sql.functions import func
from sqlalchemy.util.concurrency import asyncio

from api_app.core.config import settings
from api_app.core.schemas.users import UserCreateUpdate, PrizeCreateUpdate, PrizeResponse
from api_app.core.models.users import User, Ticket, TicketAction, Prize
from api_app.services.users import update_model_from_pydantic

log = logging.getLogger(__name__)

async def create_prize(prize: PrizeCreateUpdate, session: AsyncSession) -> Prize:
    prize = Prize(**prize.model_dump())
    prize.created_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(prize)
    await session.commit()
    return prize

async def set_prize(prize: PrizeCreateUpdate, session:AsyncSession) -> Prize:
    stmt = select(Prize).where(Prize.name == prize.name)
    result = await session.scalars(stmt)
    prize_db = result.first()
    if not prize_db:
        prize_db = await create_prize(prize, session)
    else:
        update_model_from_pydantic(prize_db, prize)
        await session.commit()

    return prize_db


async def get_prizes_and_tickets(tg_user_id:int, session: AsyncSession) -> tuple [list[Ticket], list[Prize]]:
    stmt1 = select(Prize).where(Prize.is_active == True)
    stmt2 = select(Ticket).where(Ticket.user_id==tg_user_id, Ticket.is_fired==False)

    if settings.prize.exclude_zero_quantity:
        stmt1 = stmt1.where(
            case(
                (Prize.check_quantity == True, Prize.quantity > 0),
                else_=True
            )
        )

    result1, result2 = await asyncio.gather(
        session.scalars(stmt1),
        session.scalars(stmt2)
    )
    prizes = list(result1.all())
    tickets = list(result2.all())

    if not settings.prize.exclude_zero_quantity:
        for prize in prizes:
            if prize.check_quantity and prize.quantity == 0:
                prize.weight = 0

    return tickets, prizes


async def update_prize_and_ticket(win: PrizeResponse, ticket: Ticket, session: AsyncSession) -> Prize|None:
    stmt = select(Prize).where(Prize.name == win.name)
    result = await session.scalars(stmt)
    prize = result.first()
    if not prize:
        log.exception(f"Prize {win.name} not found in database")
        return None
    if ticket:
        ticket.is_fired = True
        ticket.prize_id = prize.id
        ticket.fired_at = datetime.now(timezone.utc).replace(tzinfo=None)
    else:
        log.exception(f"Ticket is None")
    if win.check_quantity and win.quantity > 0:
        prize.quantity = win.quantity - 1
    await session.commit()
    return prize



async def get_user(tg_user_id: int, session: AsyncSession) -> User:
    stmt = select(User).where(User.id == tg_user_id)
    result = await session.scalars(stmt)
    user = result.first()

    return user


async def find_user_by_uuid(user_uuid: uuid.UUID, session: AsyncSession) -> User:
    stmt = select(User).where(User.user_uuid == user_uuid)
    result = await session.scalars(stmt)
    return result.first()


async def create_ticket_for_user(
    user_id: int,
    session: AsyncSession,
    initiator_id: int | None = None,
    action: str | None = None,
):
    ticket = Ticket(
        user_id=user_id,
        initiator_id=initiator_id,
        action=action,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    session.add(ticket)
    await session.commit()


async def get_user_tickets(
        user_id: int,
        session: AsyncSession,
):
    stmt = select(func.count()).where(Ticket.user_id == user_id)
    result = await session.scalar(stmt)

    stmt = select(Ticket.action, func.count().label("count")).where(Ticket.user_id == user_id).group_by(Ticket.action).order_by(func.count().desc())
    detail_result = await session.execute(stmt)
    detailed_tickets = detail_result.mappings().all()
    detailed_tickets = [
        {**ticket, "name": TicketAction.get_display_name(ticket["action"])}
        for ticket in detailed_tickets
    ]

    return result or 0, detailed_tickets


async def create_user(tg_user: UserCreateUpdate, session: AsyncSession) -> User:
    user = User(**tg_user.model_dump(exclude={"payload"}))
    user.created_at = datetime.now(timezone.utc).replace(tzinfo=None)
    user.last_activity = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(user)
    await session.commit()

    await create_ticket_for_user(user_id=user.id, session=session)

    return user


async def set_user(tg_user: UserCreateUpdate, session: AsyncSession) -> User:
    """
    находит пользователя по id для изменения данных о нем или создает нового
    """
    user = await get_user(tg_user.id, session=session)

    if not user:
        user = await create_user(tg_user, session)
        if tg_user.payload is not None:
            host_user = await find_user_by_uuid(tg_user.payload, session)
            if host_user is not None:
                await create_ticket_for_user(
                    user_id=host_user.id,
                    initiator_id=user.id,
                    action=TicketAction.REFERRAL,
                    session=session,
                )
    else:
        exclude = {"id", "created_at", "last_activity", "user_uuid"}
        if tg_user.phone_number is None:
            exclude.add("phone_number")
        user = update_model_from_pydantic(user, tg_user, exclude=exclude)
        user.last_activity = datetime.now(timezone.utc).replace(tzinfo=None)
        await session.commit()

    return user
