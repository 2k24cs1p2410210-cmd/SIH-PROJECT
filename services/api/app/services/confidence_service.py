from typing import Tuple


class ConfidenceService:
    """Calculates confidence score [0.0, 1.0] and ETA margin ranges."""

    PREDICTOR_WEIGHTS = {
        "ml_model": 0.95,
        "historical_avg": 0.85,
        "current_speed": 0.70,
        "schedule": 0.40,
        "unavailable": 0.0
    }

    def compute_confidence(
        self,
        predictor_type: str,
        freshness_seconds: float,
        accuracy_m: float,
        remaining_distance_m: float
    ) -> Tuple[float, str]:
        base_weight = self.PREDICTOR_WEIGHTS.get(predictor_type, 0.5)

        # Freshness penalty: loses 0.1 every 30 seconds
        freshness_factor = max(0.0, 1.0 - (freshness_seconds / 120.0))

        # Accuracy penalty: loses score if accuracy > 20m
        accuracy_factor = max(0.0, 1.0 - (accuracy_m / 50.0))

        confidence_score = round(base_weight * 0.6 + freshness_factor * 0.2 + accuracy_factor * 0.2, 2)
        confidence_score = max(0.0, min(1.0, confidence_score))

        if confidence_score >= 0.8:
            level = "high"
        elif confidence_score >= 0.5:
            level = "medium"
        else:
            level = "low"

        return confidence_score, level

    def calculate_eta_bounds(
        self,
        eta_seconds: int,
        confidence_score: float
    ) -> Tuple[int, int]:
        if eta_seconds is None:
            return None, None

        # Margin scales inversely with confidence
        margin_percent = max(0.05, 0.40 * (1.0 - confidence_score))
        min_eta = max(0, int(eta_seconds * (1.0 - margin_percent)))
        max_eta = int(eta_seconds * (1.0 + margin_percent))

        return min_eta, max_eta
