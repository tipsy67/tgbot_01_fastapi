from aiogram.utils.deep_linking import decode_payload
from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message

from tg_bot.keyboards import userkb
from tg_bot.services import api_requests

user = Router()



# START
@user.message(CommandStart(deep_link=True))
async def start_with_deep_link(message: Message, command: CommandObject):
    payload = command.args
    response = await api_requests.set_user(message.from_user, payload)

    await message.answer(
        'Для участия в розыгрыше запустите веб приложение', reply_markup=userkb.get_web_app()
    )

@user.message(CommandStart())
async def start(message: Message):
    response = await api_requests.set_user(message.from_user, None)

    await message.answer(
        'Для участия в розыгрыше запустите веб приложение', reply_markup=userkb.get_web_app()
    )


@user.message(F.contact)
async def handle_shared_contact(message: Message):
    contact = message.contact
    tg_user = message.from_user

    if tg_user.id == contact.user_id:
        response = await api_requests.set_user(contact, None)