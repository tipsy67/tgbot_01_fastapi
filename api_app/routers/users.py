from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.testing.config import db
from starlette import status

from api_app.core.db_helper import db_helper
from api_app.core.schemas.users import UserCreateUpdate, UserResponse
from api_app.crud.users import set_user, get_user

# from api_app.tasks.tg_messages import print_task

router = APIRouter()


# @router.get("/test")
# async def test():
#     await print_task.kiq()
#     return {"status": "ok"}
#
#
# @router.get("", status_code=status.HTTP_200_OK, response_model=None)
# async def get_user_rt(tg_user_id: int) -> None:
#     return await db.get_user(tg_user_id)


@router.get("", response_model=UserResponse)
async def get_user_rt(tg_user_id: int, session: AsyncSession = Depends(db_helper.session_getter)):
    user = await get_user(tg_user_id, session)
    return user

@router.post("", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def set_user_rt(tg_user: UserCreateUpdate, session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    user = await set_user(tg_user, session)
    return user

@router.get("/status")
async def get_status_rt(tg_user_id:int, session: AsyncSession = Depends(db_helper.session_getter)):
    return {"status": False}

@router.get("/tickets")
async def get_status_rt(tg_user_id:int, session: AsyncSession = Depends(db_helper.session_getter)):
    return {"tickets": 10}

