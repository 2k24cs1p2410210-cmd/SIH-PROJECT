from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async for db in get_db():
        yield db
