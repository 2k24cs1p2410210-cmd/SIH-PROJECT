from datetime import datetime, timezone
from typing import Dict, Any


def build_eta_feature_vector(
    remaining_distance_m: float,
    current_speed_mps: float,
    recorded_at: datetime
) -> Dict[str, Any]:
    """Constructs feature dictionary for ML model inference."""
    dt = recorded_at.astimezone(timezone.utc)
    return {
        "remaining_distance_m": remaining_distance_m,
        "current_speed_mps": current_speed_mps,
        "hour_of_day": dt.hour,
        "day_of_week": dt.weekday(),
        "is_weekend": 1 if dt.weekday() >= 5 else 0,
    }
