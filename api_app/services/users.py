import asyncio
import logging
import random

import aiohttp

from api_app.core.config import settings
from api_app.core.models.users import Prize
from api_app.core.schemas.tunes import RequiredChannelRequest, RequiredChannelResponse
from api_app.core.schemas.users import PrizeResponse

log = logging.getLogger(__name__)
SUBSCRIBED_STATUSES = {'member', 'administrator', 'creator'}

def update_model_from_pydantic(db_model, pydantic_model, exclude: set = None):
    """Обновляет модель БД из Pydantic модели"""
    if exclude is None:
        exclude = set()

    update_data = pydantic_model.model_dump(exclude_unset=True, exclude=exclude)
    for key, value in update_data.items():
        setattr(db_model, key, value)
    return db_model


async def check_subscription_bot_api(
    user_id: int, channels: list[RequiredChannelRequest]
) -> list[RequiredChannelResponse]|None:
    """
    Проверка подписки через Bot API
    """
    url = f"https://api.telegram.org/bot{settings.tg.token}/getChatMember"
    result_list_channels = []
    try:
        async with aiohttp.ClientSession() as session:
            for channel in channels:
                params = {'chat_id': f"@{channel.name}", 'user_id': user_id}

                async with session.get(
                        url, params=params, timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    data = await response.json()
                    if data.get('ok'):
                        result = data['result']
                        status = result['status']
                        if status in SUBSCRIBED_STATUSES:
                            result_list_channels.append(RequiredChannelResponse(name=channel.name, subscribe=True))
                        else:
                            result_list_channels.append(RequiredChannelResponse(name=channel.name, subscribe=False))
                    else:
                        result_list_channels.append(RequiredChannelResponse(name=channel.name, subscribe=False))
        return result_list_channels

    except aiohttp.ClientError as e:
        log.exception(f"HTTP error checking subscription: {e}")
    except asyncio.TimeoutError:
        log.exception("Timeout checking subscription")
    except Exception as e:
        log.exception(f"Unexpected error: {e}")

    return None


async def get_winning_prize(prizes: list[Prize]) -> tuple[PrizeResponse|None, list[PrizeResponse]]:
    """
    Выберем приз с учетом весов
    """
    if len(prizes) == 0:
        log.exception(f"Prizes are empty")
        return None, []
    list_: list[PrizeResponse] = [PrizeResponse.model_validate(prize, from_attributes=True) for prize in prizes]
    weights = [prize.weight for prize in prizes]
    win = random.choices(list_, weights=weights, k=1)[0]
    win.bingo = True

    return win, list_

