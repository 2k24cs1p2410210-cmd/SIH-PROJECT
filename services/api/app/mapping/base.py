from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple


class MapMatcher(ABC):
    """Abstract interface for map matching raw GPS coordinates to route polylines."""

    @abstractmethod
    def match_point(
        self,
        latitude: float,
        longitude: float,
        route_id: str
    ) -> Tuple[float, float, float]:
        """
        Projects (lat, lon) onto closest route segment.
        Returns: (matched_latitude, matched_longitude, distance_along_route_m)
        """
        pass
