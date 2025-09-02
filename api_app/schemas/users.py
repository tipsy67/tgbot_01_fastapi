from datetime import datetime

from pydantic import BaseModel, Field
from typing_extensions import Optional

from api_app.core.config import settings


class UserCreateUpdate(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    language_code: Optional[str] = settings.default_language_code
    token: Optional[str] = None
    ticket_id: Optional[str] = None


class UserResponse(UserCreateUpdate):
    id: int
    created_at: datetime
    last_activity: datetime
    is_staff: bool
    is_admin: bool = False



