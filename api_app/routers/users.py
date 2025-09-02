from fastapi import APIRouter
from starlette import status

from api_app.datebases import (
    users_requests as db,
)  # напрямую через функции работающие с БД
from api_app.core.schemas import (
    UserCreateUpdate,
    UserResponse,
)
from api_app.tasks.tg_messages import print_task

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/test")
async def test():
    await print_task.kiq()
    return {"status": "ok"}


@router.get("", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_rt(tg_user_id: int) -> UserResponse:
    return await db.get_user(tg_user_id)


@router.post("", status_code=status.HTTP_200_OK)
async def set_user_rt(tg_user: UserCreateUpdate) -> UserResponse:
    return await db.set_user(tg_user)





