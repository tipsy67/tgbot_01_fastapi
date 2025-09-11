"""
Settings for the API application.
"""
from pathlib import Path

from pydantic import BaseModel, PostgresDsn, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict



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

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
    tg: TGSettings = TGSettings()
    default_language_code: str = "en"
    api: ApiPrefix = ApiPrefix()
    db: DBSettings = DBSettings()
    webapp: WebAppSettings = WebAppSettings()

settings = Settings()
# print(settings.model_dump())
