import uuid

from datetime import datetime
from datetime import timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from api_app.core.schemas.users import UserCreateUpdate
from api_app.core.models.users import User, Ticket, TicketAction
from api_app.services.users import update_model_from_pydantic


async def get_user(tg_user_id: int, session: AsyncSession) -> User:
    stmt = select(User).where(User.id == tg_user_id)
    result = await session.scalars(stmt)
    user = result.first()

    return user


async def find_user_by_uuid(user_uuid: uuid.UUID, session: AsyncSession) -> User:
    stmt=select(User).where(User.user_uuid == user_uuid)
    result = await session.scalars(stmt)
    return result.first()


async def create_ticket_for_user(
        user_id: int,
        session: AsyncSession,
        initiator_id:int|None=None,
        action:str|None=None
):
    ticket = Ticket(
        user_id=user_id,
        initiator_id=initiator_id,
        action=action,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    session.add(ticket)
    await session.commit()


async def create_user(tg_user: UserCreateUpdate, session:AsyncSession) -> User:
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
                    session=session
                )
    else:
        exclude = {"id", "created_at", "last_activity", "user_uuid"}
        if tg_user.phone_number is None:
            exclude.add("phone_number")
        user = update_model_from_pydantic(user, tg_user, exclude=exclude)
        user.last_activity = datetime.now(timezone.utc).replace(tzinfo=None)
        await session.commit()

    return user


