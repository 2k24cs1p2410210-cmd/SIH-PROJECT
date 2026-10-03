from fastapi import APIRouter
from app.schemas.alert import AlertCreate, AlertResponse
from app.services.alert_service import alert_service

router = APIRouter()


@router.post(
    "/alerts",
    response_model=AlertResponse,
    summary="Create public dispatch alert",
    description="Publishes service disruption or delay alert for passengers."
)
async def create_alert(req: AlertCreate):
    return await alert_service.create_alert(req)
