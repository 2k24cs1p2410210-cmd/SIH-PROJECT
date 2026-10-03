from app.eta.current_speed_predictor import CurrentSpeedPredictor
from app.services.confidence_service import ConfidenceService


def test_current_speed_predictor():
    predictor = CurrentSpeedPredictor()
    # 5000m remaining at 10 m/s = 500s
    eta = predictor.predict(5000.0, 10.0)
    assert eta == 500


def test_confidence_service():
    service = ConfidenceService()
    score, level = service.compute_confidence("current_speed", freshness_seconds=5.0, accuracy_m=4.0, remaining_distance_m=1000.0)
    assert score > 0.5
    assert level in ["medium", "high"]
