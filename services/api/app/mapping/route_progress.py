def calculate_remaining_route_distance(
    total_route_distance_m: float,
    current_progress_m: float
) -> float:
    """Calculates remaining meters along route path."""
    return max(0.0, total_route_distance_m - current_progress_m)
