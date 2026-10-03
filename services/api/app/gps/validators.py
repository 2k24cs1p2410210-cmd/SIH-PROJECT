def is_valid_coordinate(lat: float, lon: float) -> bool:
    """Validates WGS84 latitude and longitude range."""
    return -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0


def is_acceptable_accuracy(accuracy_m: float, max_threshold_m: float = 50.0) -> bool:
    """Checks if GPS accuracy fix is within acceptable threshold in meters."""
    return 0.0 <= accuracy_m <= max_threshold_m
