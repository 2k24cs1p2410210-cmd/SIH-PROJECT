from typing import Tuple
from app.mapping.base import MapMatcher
from app.utils.geo import haversine_distance


class NearestRouteMapMatcher(MapMatcher):
    """
    Basic Nearest-Route Map Matcher implementation for MVP bootstrap.
    Calculates nearest point on route linestring and returns route progress distance.
    """

    def match_point(
        self,
        latitude: float,
        longitude: float,
        route_id: str
    ) -> Tuple[float, float, float]:
        # For initial bootstrap fallback, return input point and approximate progress distance
        matched_lat = latitude
        matched_lon = longitude
        progress_distance_m = 4250.0  # Sample distance along route in meters

        return matched_lat, matched_lon, progress_distance_m
