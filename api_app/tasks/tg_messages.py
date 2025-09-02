import datetime
import logging
from typing import Iterable

from aiogram import Bot

from api_app.core.config import settings
from api_app.core.taskiq_broker import broker, redis_source
from api_app.datebases.users_requests import get_user, get_users
from api_app.schemas.users import UserResponse
from api_app.tasks.tg_messages_utils import reference_points

logger = logging.getLogger("taskiq")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("taskiq.log")
logger.addHandler(handler)


@broker.task
async def send_message_to_speaker_task(
    initiator_id: int, recipient_id: int, text: str = None, alias_text: str = None
) -> None:
    initiator: UserResponse = await get_user(initiator_id)
    recipient: UserResponse = await get_user(recipient_id)
    if alias_text:
        full_message = alias_text


    async with Bot(token=settings.tg.token) as bot:
        await bot.send_message(recipient_id, full_message)


@broker.task
async def send_messages_to_users_task(
    recipients_ids: Iterable[int], text: str, alias_text: str = None
) -> None:
    async with Bot(token=settings.tg.token) as bot:
        recipients = await get_users(recipients_ids)
        for recipient in recipients:
            if alias_text:
                full_message = alias_text
            await bot.send_message(recipient.id, full_message)


@broker.task()
async def send_individual_message_to_users_task(user_id: int, text: str) -> None:
    async with Bot(token=settings.tg.token) as bot:
        message_id = await bot.send_message(user_id, text, parse_mode="HTML")


@broker.task
async def print_task() -> None:
    logger.warning("eeeeee !!!!")
