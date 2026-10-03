from typing import Tuple


def interpolate_coordinate(
    lat1: float, lon1: float,
    lat2: float, lon2: float,
    fraction: float
) -> Tuple[float, float]:
    """Linearly interpolates position fix between two coordinates."""
    interp_lat = lat1 + (lat2 - lat1) * fraction
    interp_lon = lon1 + (lon2 - lon1) * fraction
    return interp_lat, interp_lon
