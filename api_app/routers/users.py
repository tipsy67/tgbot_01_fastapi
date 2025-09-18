from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette import status

from api_app.core.config import settings
from api_app.core.db_helper import db_helper
from api_app.core.schemas.users import UserCreateUpdate, UserResponse, PrizeCreateUpdate, PrizeResponse
from api_app.crud.tunes import get_channels_names
from api_app.crud.users import set_user, get_user, get_user_tickets, set_prize, \
    update_prize_and_ticket, get_prizes_and_tickets
from api_app.services.users import check_subscription_bot_api, get_winning_prize

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
async def get_user_rt(
    tg_user_id: int, session: AsyncSession = Depends(db_helper.session_getter)
):
    user = await get_user(tg_user_id, session)
    return user


@router.post("", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def set_user_rt(
    tg_user: UserCreateUpdate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user = await set_user(tg_user, session)
    return user


@router.get("/status")
async def get_status_rt(
    tg_user_id: int, session: AsyncSession = Depends(db_helper.session_getter)
):
    required_channels = await get_channels_names(session)
    required_channels_result = await check_subscription_bot_api(tg_user_id, required_channels)
    subscribe_status = all([x.subscribe for x in required_channels_result])

    return {"status": subscribe_status, "required_channels": required_channels_result}


@router.get("/tickets")
async def get_status_rt(
    tg_user_id: int, session: AsyncSession = Depends(db_helper.session_getter)
):
    tickets, detailed_tickets = await get_user_tickets(tg_user_id, session)
    return {"tickets": tickets, "detailed_tickets": detailed_tickets}

@router.get("/prizes")
async def get_prizes_rt(tg_user_id:int, first_fetch:bool=False, session: AsyncSession = Depends(db_helper.session_getter)):
    list_tickets, list_prizes = await get_prizes_and_tickets(tg_user_id, session)
    # spins_left = len(list_tickets)
    if not first_fetch:
        win, list_prizes = await get_winning_prize(list_prizes)
        await update_prize_and_ticket(win, next(iter(list_tickets), None), session)
        # spins_left -= spins_left
    else:
        list_prizes = [PrizeResponse.model_validate(item, from_attributes=True) for item in list_prizes]
    return {"prizes": list_prizes, "spins_left": len(list_tickets)}

@router.post("/prizes")
async def set_prize_rt(prize:PrizeCreateUpdate , session:AsyncSession = Depends(db_helper.session_getter)):
    return {"prize": await set_prize(prize, session)}
