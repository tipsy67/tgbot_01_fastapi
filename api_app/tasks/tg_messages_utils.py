import datetime

from api_app.core.models.users import Prize, Ticket
from api_app.core.taskiq_broker import redis_source
from api_app.tasks.tg_messages import send_individual_message_to_users_task


async def get_target_time(
        delta_time: datetime.timedelta
) -> datetime.datetime:
    current_time = datetime.datetime.now(datetime.timezone.utc)
    target_time = current_time + delta_time
    return target_time


async def send_prize_info_to_user(prize:Prize, ticket:Ticket):
    text = f"🎉 Поздравляем! \nВаш приз {prize.name}.\nНомер выигравшего билета {ticket.id}"
    target_time = await get_target_time(datetime.timedelta(minutes=1))
    await send_individual_message_to_users_task.schedule_by_time (redis_source, target_time, user_id=ticket.user_id, text=text)
