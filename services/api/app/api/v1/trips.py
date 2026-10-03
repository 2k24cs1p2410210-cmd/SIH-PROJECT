from fastapi import APIRouter
from app.schemas.trip import StartTripRequest, TripResponse
from app.services.trip_service import trip_service

router = APIRouter()


@router.post(
    "/trips/start",
    response_model=TripResponse,
    summary="Start a new driver trip",
    description="Initializes trip session for a bus on a specific route."
)
async def start_trip(req: StartTripRequest):
    return await trip_service.start_trip(req)


@router.post(
    "/trips/end",
    response_model=TripResponse,
    summary="End an active driver trip",
    description="Terminates active trip session and archives trajectory."
)
async def end_trip(trip_id: str):
    return await trip_service.end_trip(trip_id)
