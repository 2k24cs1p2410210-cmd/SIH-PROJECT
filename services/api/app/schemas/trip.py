from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StartTripRequest(BaseModel):
    bus_id: str
    route_id: str
    driver_id: Optional[str] = None


class TripResponse(BaseModel):
    trip_id: str
    bus_id: str
    route_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
