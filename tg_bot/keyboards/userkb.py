import os
from datetime import datetime

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           WebAppInfo)


def get_web_app():
    url_webapp=os.environ.get("WEBAPP__URL")
    timestamp = int(datetime.now().timestamp())
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть WebApp",
                    web_app=WebAppInfo(
                        url=f"{url_webapp}/index.html?force_reload={timestamp}"
                    ),
                )
            ]
        ]
    )
    return keyboard


