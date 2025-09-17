"""
Settings for the API application.
"""
import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

class LoggingSettings(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class TGSettings(BaseModel):
    token: str = ""


class DBSettings(BaseModel):
    url: PostgresDsn = ""
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


class WebAppSettings(BaseModel):
    url: str = ""

class PrizeSettings(BaseModel):
    exclude_zero_quantity: bool = False
    weight_upper_limit: int = 50

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
    api: ApiPrefix = ApiPrefix()
    default_language_code: str = "en"
    db: DBSettings = DBSettings()
    logging:LoggingSettings = LoggingSettings()
    prize: PrizeSettings = PrizeSettings()
    tg: TGSettings = TGSettings()
    webapp: WebAppSettings = WebAppSettings()


settings = Settings()
# print(settings.model_dump())
