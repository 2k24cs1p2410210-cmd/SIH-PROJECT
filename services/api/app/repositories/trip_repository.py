from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.trip import Trip


class TripRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, trip_id: uuid.UUID) -> Optional[Trip]:
        stmt = select(Trip).where(Trip.id == trip_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
