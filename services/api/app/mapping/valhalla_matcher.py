from typing import Tuple
from app.mapping.base import MapMatcher


class ValhallaMapMatcher(MapMatcher):
    """
    Placeholder adapter for future self-hosted Valhalla / Meili map matching engine integration.
    Do not run or deploy Valhalla yet; documented as future service upgrade.
    """

    def __init__(self, valhalla_url: str = "http://localhost:8002"):
        self.valhalla_url = valhalla_url

    def match_point(
        self,
        latitude: float,
        longitude: float,
        route_id: str
    ) -> Tuple[float, float, float]:
        # TODO: Implement Valhalla Meili HTTP RPC trace_attributes call when Valhalla server is deployed
        return latitude, longitude, 0.0
