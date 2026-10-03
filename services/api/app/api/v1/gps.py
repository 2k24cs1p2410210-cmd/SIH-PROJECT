from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.gps import GpsUpdateInput, GpsUpdateResponse
from app.services.gps_ingestion_service import gps_ingestion_service

router = APIRouter()


@router.post(
    "/gps/update",
    response_model=GpsUpdateResponse,
    summary="Ingest driver GPS fix",
    description="Validates, cleans, projects onto route, updates ETA, persists to PostGIS, and broadcasts real-time position fix to WebSocket clients."
)
async def update_gps_location(
    data: GpsUpdateInput,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await gps_ingestion_service.process_gps_update(data, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest GPS point: {str(exc)}"
        )

