from typing import Optional, List, Dict, Any
from app.utils.geo import haversine_distance


class StopMatcher:
    """Matches bus location to upcoming stops along the active route sequence."""

    def find_next_stop(
        self,
        current_lat: float,
        current_lon: float,
        stops: List[Dict[str, Any]],
        arrival_radius_m: float = 30.0
    ) -> Optional[Dict[str, Any]]:
        for stop in stops:
            dist_m = haversine_distance(current_lat, current_lon, stop["latitude"], stop["longitude"])
            if dist_m > arrival_radius_m:
                return stop
        return stops[0] if stops else None
