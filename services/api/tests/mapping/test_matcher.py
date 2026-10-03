from app.mapping.nearest_route_matcher import NearestRouteMapMatcher


def test_nearest_route_matcher():
    matcher = NearestRouteMapMatcher()
    lat, lon, dist = matcher.match_point(15.3647, 75.1239, "route-001")
    assert lat == 15.3647
    assert lon == 75.1239
    assert dist >= 0.0
