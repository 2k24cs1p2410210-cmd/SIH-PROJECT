from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class IncidentCreate(BaseModel):
    trip_id: Optional[str] = None
    bus_id: Optional[str] = None
    incident_type: str
    description: Optional[str] = None


class IncidentResponse(BaseModel):
    id: str
    trip_id: Optional[str] = None
    bus_id: Optional[str] = None
    incident_type: str
    description: Optional[str] = None
    status: str
    reported_at: datetime
