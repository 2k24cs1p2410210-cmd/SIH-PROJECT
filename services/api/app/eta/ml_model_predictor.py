from typing import Optional, Dict, Any
from app.eta.base import ETAPredictor


class MLModelPredictor(ETAPredictor):
    """
    XGBoost ML ETA Predictor placeholder.
    Enabled when sufficient (>50) historical trip records are present.
    """

    @property
    def name(self) -> str:
        return "ml_model"

    def predict(
        self,
        remaining_distance_m: float,
        current_speed_mps: float,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[int]:
        # TODO: Load XGBoost model artifact and run inference on feature vector
        if context and "ml_predicted_seconds" in context:
            return int(context["ml_predicted_seconds"])
        return None
