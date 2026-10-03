from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class ETAPredictor(ABC):
    """Abstract base class for all ETA predictors in TransitPulse AI."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name identifier of the predictor."""
        pass

    @abstractmethod
    def predict(
        self,
        remaining_distance_m: float,
        current_speed_mps: float,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[int]:
        """
        Calculate estimated time of arrival in seconds.
        Returns None if predictor is unable to generate prediction.
        """
        pass
