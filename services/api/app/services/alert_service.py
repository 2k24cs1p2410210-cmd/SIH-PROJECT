from datetime import datetime, timezone
import uuid
from app.schemas.alert import AlertCreate, AlertResponse


class AlertService:
    async def create_alert(self, req: AlertCreate) -> AlertResponse:
        return AlertResponse(
            id=str(uuid.uuid4()),
            title=req.title,
            message=req.message,
            severity=req.severity,
            route_id=req.route_id,
            created_at=datetime.now(timezone.utc)
        )


alert_service = AlertService()
