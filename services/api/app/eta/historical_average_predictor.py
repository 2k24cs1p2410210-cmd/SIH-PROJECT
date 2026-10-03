from typing import Optional, Dict, Any
from app.eta.base import ETAPredictor


class HistoricalAveragePredictor(ETAPredictor):
    """
    Historical Segment Average ETA Predictor placeholder.
    Used when at least 10 completed historical segment traversals exist.
    """

    @property
    def name(self) -> str:
        return "historical_avg"

    def predict(
        self,
        remaining_distance_m: float,
        current_speed_mps: float,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[int]:
        # TODO: Implement segment query from database when historical trip logs reach threshold
        if context and "historical_segment_avg_seconds" in context:
            return int(context["historical_segment_avg_seconds"])
        return None
