from pydantic import BaseModel
from typing import Optional, List, Any


class RouteResponse(BaseModel):
    id: str
    route_code: str
    name: str
    origin_name: Optional[str] = None
    destination_name: Optional[str] = None
    distance_meters: float = 0.0
    coordinates: Optional[List[List[float]]] = None


class RouteListResponse(BaseModel):
    total: int
    routes: List[RouteResponse]
