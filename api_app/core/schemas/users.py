from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from api_app.core.config import settings


class UserCreateUpdate(BaseModel):
    id: int
    username: str|None = None
    first_name: str
    last_name: str|None = None
    phone_number: str|None = None
    language_code: str|None= settings.default_language_code
    payload: UUID|None = None

class UserResponse(UserCreateUpdate):
    entrant_id: int
    created_at: datetime
    last_activity: datetime
    user_uuid: UUID
    is_staff: bool = False
    is_admin: bool = False



