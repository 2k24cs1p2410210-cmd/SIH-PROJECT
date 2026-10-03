from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AlertCreate(BaseModel):
    title: str
    message: str
    severity: str = "warning"
    route_id: Optional[str] = None


class AlertResponse(BaseModel):
    id: str
    title: str
    message: str
    severity: str
    route_id: Optional[str] = None
    created_at: datetime
