from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from api_app.core.config import settings


class UserCreateUpdate(BaseModel):
    id: int
    username: str | None = None
    first_name: str
    last_name: str | None = None
    phone_number: str | None = None
    language_code: str | None = settings.default_language_code
    payload: UUID | None = None


class UserResponse(UserCreateUpdate):
    entrant_id: int
    created_at: datetime
    last_activity: datetime
    user_uuid: UUID
    is_staff: bool = False
    is_admin: bool = False

class PrizeCreateUpdate(BaseModel):
    name: str = Field(max_length=50)
    is_active: bool = Field(default=False)
    weight: int = Field(default=1, ge=0, description="Weight must be between 1 and 50")
    description: str = Field(max_length=255, default="")
    quantity: int = Field(default=0)
    check_quantity: bool = Field(default=False)

    @field_validator('weight')
    @classmethod
    def validate_weight(cls, v):
        if v > settings.prize.weight_upper_limit:
            raise ValueError(
                f"Weight must be <= {settings.prize.weight_upper_limit}"
            )
        return v

class PrizeResponse(BaseModel):
    name: str = Field(max_length=50)
    bingo: bool = Field(default=False)
    quantity: int = Field(default=0)
    check_quantity: bool = Field(default=False)
