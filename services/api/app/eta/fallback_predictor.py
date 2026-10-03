from typing import Tuple, Optional, Dict, Any
from app.eta.base import ETAPredictor
from app.eta.current_speed_predictor import CurrentSpeedPredictor
from app.eta.historical_average_predictor import HistoricalAveragePredictor
from app.eta.ml_model_predictor import MLModelPredictor


class FallbackETAPredictor:
    """
    Orchestrates ETA predictors in hierarchy order:
    1. ML Model (if enough trip data exists)
    2. Historical Segment Average (if segment traversals exist)
    3. Current Speed Baseline (default working baseline)
    4. Schedule Fallback
    5. Unavailable / Low-confidence state
    """

    def __init__(self):
        self.ml_predictor = MLModelPredictor()
        self.hist_predictor = HistoricalAveragePredictor()
        self.speed_predictor = CurrentSpeedPredictor()

    def predict_eta(
        self,
        remaining_distance_m: float,
        current_speed_mps: float,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[Optional[int], str]:
        # Tier 1: ML Model
        eta = self.ml_predictor.predict(remaining_distance_m, current_speed_mps, context)
        if eta is not None:
            return eta, self.ml_predictor.name

        # Tier 2: Historical Segment Average
        eta = self.hist_predictor.predict(remaining_distance_m, current_speed_mps, context)
        if eta is not None:
            return eta, self.hist_predictor.name

        # Tier 3: Current Speed Baseline
        eta = self.speed_predictor.predict(remaining_distance_m, current_speed_mps, context)
        if eta is not None:
            return eta, self.speed_predictor.name

        # Tier 4/5: Schedule or Unavailable
        return None, "unavailable"
