from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from tg_bot.keyboards import userkb

user = Router()



# START
@user.message(CommandStart())
async def start(message: Message):
    # response = await api_requests.set_user(message.from_user)

    await message.answer(
        'Для участия в розыгрыше запустите веб приложение', reply_markup=userkb.get_web_app()
    )
