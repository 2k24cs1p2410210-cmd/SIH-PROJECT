from sqlalchemy.ext.asyncio import AsyncSession
from app.models.prediction import Prediction


class PredictionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_prediction(self, prediction: Prediction) -> Prediction:
        self.session.add(prediction)
        await self.session.commit()
        return prediction
