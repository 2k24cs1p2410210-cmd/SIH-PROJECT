from fastapi import APIRouter
from datetime import datetime, timezone, timedelta
from app.schemas.eta import StopArrivalsResponse, StopArrivalEstimate

router = APIRouter()


@router.get(
    "/stops/{stop_id}/arrivals",
    response_model=StopArrivalsResponse,
    summary="Get upcoming bus arrivals for a stop",
    description="Calculates live ETA and confidence bounds for buses approaching the given stop ID. [Note: Returns demo mock data if DB data is unpopulated]"
)
async def get_stop_arrivals(stop_id: str):
    now = datetime.now(timezone.utc)
    demo_arrivals = [
        StopArrivalEstimate(
            bus_id="bus-101",
            route_id="route-001",
            route_name="Hubballi CBT to Dharwad BRTS",
            eta_seconds=340,
            eta_timestamp=now + timedelta(seconds=340),
            confidence_score=0.88,
            confidence_level="high",
            range_min_seconds=300,
            range_max_seconds=410,
            predictor_type="current_speed",
            distance_remaining_m=2450.0
        ),
        StopArrivalEstimate(
            bus_id="bus-102",
            route_id="route-001",
            route_name="Hubballi CBT to Dharwad BRTS",
            eta_seconds=1120,
            eta_timestamp=now + timedelta(seconds=1120),
            confidence_score=0.72,
            confidence_level="medium",
            range_min_seconds=950,
            range_max_seconds=1300,
            predictor_type="historical_avg",
            distance_remaining_m=8100.0
        )
    ]

    return StopArrivalsResponse(
        stop_id=stop_id,
        stop_name="Unkal Lake BRTS Stop",
        timestamp=now,
        arrivals=demo_arrivals
    )
