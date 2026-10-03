from typing import Optional, Dict, Any
from app.eta.base import ETAPredictor


class CurrentSpeedPredictor(ETAPredictor):
    """
    Primary baseline predictor.
    Calculates ETA using remaining distance and current speed with practical speed bounds.
    """

    MIN_SPEED_MPS = 2.0  # ~7.2 km/h fallback min speed
    MAX_SPEED_MPS = 22.2  # ~80 km/h max urban speed cap

    @property
    def name(self) -> str:
        return "current_speed"

    def predict(
        self,
        remaining_distance_m: float,
        current_speed_mps: float,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[int]:
        if remaining_distance_m <= 0:
            return 0

        # Apply bounds to speed
        effective_speed = max(current_speed_mps, self.MIN_SPEED_MPS)
        effective_speed = min(effective_speed, self.MAX_SPEED_MPS)

        eta_seconds = int(remaining_distance_m / effective_speed)
        return eta_seconds
