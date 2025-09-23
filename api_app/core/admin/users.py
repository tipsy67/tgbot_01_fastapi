from sqladmin import ModelView

from api_app.core.models.users import User, Prize, Ticket


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.first_name, User.last_name, User.username]
    icon = "fa-solid fa-user"

class TicketAdmin(ModelView, model=Ticket):
    column_list = [Ticket.id, Ticket.user_id, Ticket.prize]
    icon = "fa-solid fa-ticket-alt"

class PrizeAdmin(ModelView, model=Prize):
    column_list = [Prize.id, Prize.name, Prize.is_active, Prize.weight, Prize.quantity, Prize.check_quantity]
    icon = "fa-solid fa-gift"