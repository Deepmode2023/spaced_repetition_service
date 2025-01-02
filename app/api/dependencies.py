from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastucture.db.session import get_session


async def session() -> AsyncSession:
    async with get_session() as connect:
        return connect
