from datetime import datetime
from typing import Iterable

from fastapi import HTTPException

from starlette import status


from api_app.schemas.users import (
    UserCreateUpdate,
    UserResponse,
)


async def get_user(tg_user_id: int) -> UserResponse:
    pass



async def get_users(recipients_ids: Iterable[int]) -> list[UserResponse]:
    pass


async def set_user(tg_user: UserCreateUpdate) -> UserResponse:
    """
    находит пользователя по tg_id для изменения данных о нем или создает нового
    """
    pass


