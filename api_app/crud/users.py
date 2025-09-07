from typing import Iterable
from datetime import datetime
from datetime import timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from api_app.core.schemas.users import UserResponse, UserCreateUpdate
from api_app.core.models.users import User


async def get_user(tg_user_id: int) -> UserResponse:
    pass



async def get_users(recipients_ids: Iterable[int]) -> list[UserResponse]:
    pass


async def set_user(tg_user: UserCreateUpdate, session: AsyncSession) -> User:
    """
    находит пользователя по tg_id для изменения данных о нем или создает нового
    """
    stmt = select(User).where(User.id == tg_user.id)
    result = await session.scalars(stmt)
    user = result.first()

    if not user:
        user = User(**tg_user.model_dump())
        user.created_at = datetime.now(timezone.utc).replace(tzinfo=None)
        user.last_activity = datetime.now(timezone.utc).replace(tzinfo=None)
        session.add(user)
    else:
        user.last_activity = datetime.now(timezone.utc).replace(tzinfo=None)

    await session.commit()

    return user


