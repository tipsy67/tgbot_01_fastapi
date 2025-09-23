from sqladmin import ModelView

from api_app.core.models.tunes import RequiredChannel


class RequiredChannelAdmin(ModelView, model=RequiredChannel):
    column_list = [RequiredChannel.name, RequiredChannel.is_active]
    icon = "fa-solid fa-puzzle-piece"