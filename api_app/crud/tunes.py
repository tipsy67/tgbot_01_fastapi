from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from api_app.core.models.tunes import RequiredChannel
from api_app.core.schemas.tunes import RequiredChannelRequest


async def get_channels(
        session: AsyncSession
) -> list[RequiredChannel]|None:
    stmt = select(RequiredChannel).where(RequiredChannel.is_active == True)
    result = await session.scalars(stmt)
    required_channels_orm = result.all()
    if not required_channels_orm:
        return None
    return list(required_channels_orm)


async def get_channels_names(
        session: AsyncSession
) -> list[RequiredChannelRequest]|None:
    required_channels_orm = await get_channels(session=session)
    if not required_channels_orm:
        return None
    required_channels = [RequiredChannelRequest.model_validate(x , from_attributes=True) for x in required_channels_orm]
    return required_channels