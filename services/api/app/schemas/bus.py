from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class LiveBusResponse(BaseModel):
    bus_id: str
    registration_number: str
    route_id: Optional[str] = None
    route_name: Optional[str] = None
    trip_id: Optional[str] = None
    latitude: float
    longitude: float
    speed_kmh: float
    heading: float
    last_updated: datetime
    status: str = "in_transit"
    occupancy_level: str = "medium"
    seconds_since_update: Optional[int] = None


class LiveBusListResponse(BaseModel):
    total: int
    timestamp: datetime
    buses: List[LiveBusResponse]
