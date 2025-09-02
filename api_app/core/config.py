"""
Settings for the API application.
"""

from enum import Enum

from pydantic import AmqpDsn, BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class TGSettings(BaseModel):
    token: str = ""

class DBSettings(BaseModel):
        url: PostgresDsn
        echo: bool = False
        echo_pool: bool = False
        pool_size: int = 50
        max_overflow: int = 10

        naming_convention: dict[str, str] = {
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            "api_app/.env",
            "api_app/.env.dan",
            # "api_app/.env.production",
        ),  # todo: убрать прямой путь и сделать относительный путь
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )
    tg: TGSettings = TGSettings()
    default_language_code: str = "en"


settings = Settings()
# print(settings.model_dump())
