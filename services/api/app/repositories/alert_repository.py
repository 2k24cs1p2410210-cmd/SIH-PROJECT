from sqlalchemy.ext.asyncio import AsyncSession
from app.models.alert import Alert


class AlertRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_alert(self, alert: Alert) -> Alert:
        self.session.add(alert)
        await self.session.commit()
        return alert
