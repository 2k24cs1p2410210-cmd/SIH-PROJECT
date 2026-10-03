from typing import Dict, Any, Optional
from app.gps.validators import is_valid_coordinate, is_acceptable_accuracy
from app.gps.outlier_detection import is_speed_jump


class GPSCleaner:
    """GPS data cleaning pipeline performing validation, jitter removal, and outlier detection."""

    def clean_point(
        self,
        lat: float,
        lon: float,
        accuracy_m: float,
        speed_mps: float,
        prev_point: Optional[Dict[str, Any]] = None
    ) -> bool:
        if not is_valid_coordinate(lat, lon):
            return False

        if accuracy_m > 50.0:  # Ignore noisy GPS fixes
            return False

        if prev_point:
            prev_lat = prev_point["latitude"]
            prev_lon = prev_point["longitude"]
            prev_time = prev_point["timestamp_epoch"]
            curr_time = prev_point.get("current_timestamp_epoch", prev_time + 5)

            if is_speed_jump(prev_lat, prev_lon, prev_time, lat, lon, curr_time):
                return False

        return True
