from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List
from app.eta.fallback_predictor import FallbackETAPredictor
from app.services.confidence_service import ConfidenceService


class ETAService:
    """Service layer orchestrating ETA calculation and confidence assignment."""

    def __init__(self):
        self.fallback_predictor = FallbackETAPredictor()
        self.confidence_service = ConfidenceService()

    def calculate_stop_eta(
        self,
        remaining_distance_m: float,
        current_speed_mps: float,
        freshness_seconds: float = 5.0,
        accuracy_m: float = 5.0
    ) -> Dict[str, Any]:
        eta_seconds, predictor_type = self.fallback_predictor.predict_eta(
            remaining_distance_m, current_speed_mps
        )

        confidence_score, confidence_level = self.confidence_service.compute_confidence(
            predictor_type, freshness_seconds, accuracy_m, remaining_distance_m
        )

        min_eta, max_eta = self.confidence_service.calculate_eta_bounds(
            eta_seconds, confidence_score
        )

        eta_timestamp = None
        if eta_seconds is not None:
            eta_timestamp = datetime.now(timezone.utc) + timedelta(seconds=eta_seconds)

        return {
            "eta_seconds": eta_seconds,
            "eta_timestamp": eta_timestamp,
            "confidence_score": confidence_score,
            "confidence_level": confidence_level,
            "range_min_seconds": min_eta,
            "range_max_seconds": max_eta,
            "predictor_type": predictor_type,
            "distance_remaining_m": remaining_distance_m
        }


eta_service = ETAService()
