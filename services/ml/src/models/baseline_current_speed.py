class BaselineCurrentSpeedModel:
    """Current Speed ETA baseline model for ML pipeline benchmarking."""

    def __init__(self, min_speed_mps: float = 2.0):
        self.min_speed_mps = min_speed_mps

    def predict(self, remaining_distance_m: float, current_speed_mps: float) -> float:
        speed = max(current_speed_mps, self.min_speed_mps)
        return remaining_distance_m / speed
