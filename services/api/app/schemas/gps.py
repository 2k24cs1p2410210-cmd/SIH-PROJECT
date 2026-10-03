from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class GpsUpdateInput(BaseModel):
    trip_id: str = Field(..., description="ID of the active trip")
    bus_id: str = Field(..., description="Bus registration/device code")
    latitude: float = Field(..., ge=-90.0, le=90.0, description="WGS84 latitude")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="WGS84 longitude")
    altitude: Optional[float] = Field(None, description="Altitude in meters")
    speed_mps: float = Field(0.0, ge=0.0, description="Speed in meters per second")
    heading: float = Field(0.0, ge=0.0, le=360.0, description="Heading degree 0-360")
    accuracy_m: float = Field(0.0, ge=0.0, description="GPS horizontal accuracy in meters")
    recorded_at: datetime = Field(..., description="UTC timestamp recorded on device")
    battery_level: Optional[int] = Field(None, ge=0, le=100)


class GpsUpdateResponse(BaseModel):
    status: str = "success"
    point_id: Optional[int] = None
    is_processed: bool = True
    route_distance_m: Optional[float] = None
    eta_updated: bool = True
    accepted_count: int = 1
    rejected_count: int = 0
    persisted_count: int = 0

