from aiogram.utils.deep_linking import decode_payload
from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message

from tg_bot.keyboards import userkb
from tg_bot.services import api_requests

user = Router()



# START
@user.message(CommandStart(deep_link=True))
async def start(message: Message, command: CommandObject):
    payload = command.args
    response = await api_requests.set_user(message.from_user, payload)

    await message.answer(
        'Для участия в розыгрыше запустите веб приложение', reply_markup=userkb.get_web_app()
    )
