import logging
from typing import Iterable

from aiogram import Bot

from api_app.core.config import settings
from api_app.core.taskiq_broker import broker


logger = logging.getLogger("taskiq")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("taskiq.log")
logger.addHandler(handler)


@broker.task()
async def send_individual_message_to_users_task(user_id: int, text: str) -> None:
    async with Bot(token=settings.tg.token) as bot:
        message_id = await bot.send_message(user_id, text, parse_mode="HTML")


@broker.task
async def print_task() -> None:
    logger.warning("eeeeee !!!!")
