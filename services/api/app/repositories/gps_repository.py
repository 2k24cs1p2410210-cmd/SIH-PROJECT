import logging
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.gps_point import GpsPoint

logger = logging.getLogger(__name__)


class GpsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_point(self, point: GpsPoint) -> GpsPoint:
        try:
            self.session.add(point)
            await self.session.commit()
            await self.session.refresh(point)
            return point
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error persisting GpsPoint to database: {e}")
            raise

    async def add_points(self, points: List[GpsPoint]) -> List[GpsPoint]:
        if not points:
            return []
        try:
            self.session.add_all(points)
            await self.session.commit()
            for p in points:
                await self.session.refresh(p)
            return points
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error batch persisting GpsPoints to database: {e}")
            raise

