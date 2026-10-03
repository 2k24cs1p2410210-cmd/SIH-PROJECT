from app.utils.geo import haversine_distance


def is_speed_jump(
    lat1: float, lon1: float, time1_epoch: float,
    lat2: float, lon2: float, time2_epoch: float,
    max_speed_kmh: float = 120.0
) -> bool:
    """Detects unrealistic spatial jumps or teleportation anomalies (>120 km/h)."""
    time_delta_sec = time2_epoch - time1_epoch
    if time_delta_sec <= 0:
        return True  # Invalid or non-increasing timestamp

    distance_m = haversine_distance(lat1, lon1, lat2, lon2)
    speed_mps = distance_m / time_delta_sec
    speed_kmh = speed_mps * 3.6

    return speed_kmh > max_speed_kmh
