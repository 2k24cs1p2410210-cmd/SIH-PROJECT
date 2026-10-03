from fastapi import APIRouter
from datetime import datetime, timezone
from app.schemas.incident import IncidentCreate, IncidentResponse

router = APIRouter()


@router.post(
    "/incidents",
    response_model=IncidentResponse,
    summary="Report driver breakdown or traffic incident",
    description="Logs incident report for fleet management."
)
async def report_incident(req: IncidentCreate):
    return IncidentResponse(
        id="inc-demo-01",
        trip_id=req.trip_id,
        bus_id=req.bus_id,
        incident_type=req.incident_type,
        description=req.description,
        status="active",
        reported_at=datetime.now(timezone.utc)
    )
