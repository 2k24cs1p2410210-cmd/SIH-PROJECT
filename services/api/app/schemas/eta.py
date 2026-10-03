from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class StopArrivalEstimate(BaseModel):
    bus_id: str
    route_id: str
    route_name: str
    eta_seconds: Optional[int] = None
    eta_timestamp: Optional[datetime] = None
    confidence_score: float = 0.5
    confidence_level: str = "medium"  # low, medium, high
    range_min_seconds: Optional[int] = None
    range_max_seconds: Optional[int] = None
    predictor_type: str = "current_speed"  # ml_model, historical_avg, current_speed, schedule
    distance_remaining_m: float = 0.0


class StopArrivalsResponse(BaseModel):
    stop_id: str
    stop_name: str
    timestamp: datetime
    arrivals: List[StopArrivalEstimate]
