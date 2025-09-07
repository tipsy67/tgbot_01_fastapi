import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

from handlers.user import user


async def main():
    bot = Bot(token=os.environ.get("TG__TOKEN"))  # , session=session)
    dp = Dispatcher()
    dp.include_routers(
        user,
    )
    await dp.start_polling(bot)



if __name__ == "__main__":
    print("Bot starting...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot canceled.")
