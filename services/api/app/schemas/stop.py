from pydantic import BaseModel
from typing import Optional, List


class StopResponse(BaseModel):
    id: str
    stop_code: Optional[str] = None
    name: str
    route_id: str
    sequence_order: int
    latitude: float
    longitude: float
