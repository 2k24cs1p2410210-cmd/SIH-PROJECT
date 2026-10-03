from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.route import Route


class RouteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Route]:
        stmt = select(Route)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
