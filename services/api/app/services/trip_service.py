from datetime import datetime, timezone
import uuid
from app.schemas.trip import StartTripRequest, TripResponse


class TripService:
    async def start_trip(self, req: StartTripRequest) -> TripResponse:
        new_id = str(uuid.uuid4())
        return TripResponse(
            trip_id=new_id,
            bus_id=req.bus_id,
            route_id=req.route_id,
            status="active",
            start_time=datetime.now(timezone.utc)
        )

    async def end_trip(self, trip_id: str) -> TripResponse:
        return TripResponse(
            trip_id=trip_id,
            bus_id="bus-101",
            route_id="route-001",
            status="completed",
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc)
        )


trip_service = TripService()
