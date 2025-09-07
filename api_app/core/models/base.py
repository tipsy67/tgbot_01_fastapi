from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.schema import MetaData

from api_app.core.config import settings


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )