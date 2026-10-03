from fastapi import APIRouter
from app.schemas.route import RouteListResponse, RouteResponse

router = APIRouter()

DEMO_ROUTES = [
    RouteResponse(
        id="route-001",
        route_code="BRTS-1",
        name="Hubballi CBT to Dharwad BRTS",
        origin_name="Hubballi CBT",
        destination_name="Dharwad Bus Stand",
        distance_meters=21500.0,
        coordinates=[
            [75.123955, 15.364708],
            [75.091500, 15.391200],
            [75.051200, 15.421500],
            [75.012500, 15.458900]
        ]
    ),
    RouteResponse(
        id="route-002",
        route_code="R-12",
        name="Old Bus Stand to Navanagar Circle",
        origin_name="Old Bus Stand",
        destination_name="Navanagar Circle",
        distance_meters=9800.0,
        coordinates=[
            [75.132000, 15.352000],
            [75.110000, 15.375000],
            [75.091500, 15.391200]
        ]
    )
]


@router.get(
    "/routes",
    response_model=RouteListResponse,
    summary="Get all transit routes",
    description="Returns list of configured public transit routes with line coordinates. [Note: Returns demo mock data if DB data is unpopulated]"
)
async def get_routes():
    return RouteListResponse(
        total=len(DEMO_ROUTES),
        routes=DEMO_ROUTES
    )
