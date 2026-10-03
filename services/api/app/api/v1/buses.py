import json
import logging
from typing import Optional, List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.redis import get_redis
from app.schemas.bus import LiveBusListResponse, LiveBusResponse
from app.models.gps_point import GpsPoint
from app.models.trip import Trip

router = APIRouter()
logger = logging.getLogger(__name__)

# Deterministic demo buses data for bootstrapping fallback
DEMO_LIVE_BUSES = [
    LiveBusResponse(
        bus_id="bus-101",
        registration_number="KA-25-F-1001",
        route_id="route-001",
        route_name="Hubballi CBT to Dharwad BRTS",
        trip_id="trip-demo-01",
        latitude=15.364708,
        longitude=75.123955,
        speed_kmh=32.5,
        heading=142.0,
        last_updated=datetime.now(timezone.utc),
        seconds_since_update=0,
        status="in_transit",
        occupancy_level="medium"
    ),
    LiveBusResponse(
        bus_id="bus-102",
        registration_number="KA-25-F-1002",
        route_id="route-001",
        route_name="Hubballi CBT to Dharwad BRTS",
        trip_id="trip-demo-02",
        latitude=15.421500,
        longitude=75.051200,
        speed_kmh=28.0,
        heading=310.0,
        last_updated=datetime.now(timezone.utc),
        seconds_since_update=0,
        status="in_transit",
        occupancy_level="high"
    ),
    LiveBusResponse(
        bus_id="bus-201",
        registration_number="KA-25-F-2001",
        route_id="route-002",
        route_name="Old Bus Stand to Navanagar Circle",
        trip_id="trip-demo-03",
        latitude=15.391200,
        longitude=75.091500,
        speed_kmh=0.0,
        heading=90.0,
        last_updated=datetime.now(timezone.utc),
        seconds_since_update=0,
        status="stopped_at_station",
        occupancy_level="low"
    )
]


def _build_bus_response(data: dict, now: datetime) -> Optional[LiveBusResponse]:
    try:
        ts_str = data.get("timestamp")
        if not ts_str:
            return None
        recorded_at = datetime.fromisoformat(ts_str)
        if recorded_at.tzinfo is None:
            recorded_at = recorded_at.replace(tzinfo=timezone.utc)
        
        seconds_since = max(0, int((now - recorded_at).total_seconds()))
        bus_id = str(data.get("bus_id", "unknown"))
        speed_mps = float(data.get("speed", 0.0))
        speed_kmh = round(speed_mps * 3.6, 1)

        return LiveBusResponse(
            bus_id=bus_id,
            registration_number=f"KA-25-{bus_id}",
            route_id=str(data.get("route_id", "route-001")),
            route_name=f"Route {data.get('route_id', '001')}",
            trip_id=str(data.get("trip_id")) if data.get("trip_id") else None,
            latitude=float(data["lat"]),
            longitude=float(data["lon"]),
            speed_kmh=speed_kmh,
            heading=float(data.get("bearing", 0.0)),
            last_updated=recorded_at,
            seconds_since_update=seconds_since,
            status="in_transit",
            occupancy_level="medium"
        )
    except Exception as exc:
        logger.warning(f"Error parsing Redis bus location data: {exc}")
        return None


@router.get(
    "/buses/live",
    response_model=LiveBusListResponse,
    summary="Get live active buses",
    description="Returns all active buses emitting live GPS location fixes from Redis cache, with DB/demo fallback."
)
async def get_live_buses(
    route_id: Optional[str] = Query(None, description="Filter live buses by route ID"),
    db: Optional[AsyncSession] = Depends(get_db)
):
    now = datetime.now(timezone.utc)
    buses: List[LiveBusResponse] = []

    # 1. Try fetching from Redis
    try:
        redis = await get_redis()
        if redis is not None:
            if route_id:
                bus_ids = await redis.smembers(f"route:{route_id}:buses")
                keys = [f"bus:{bid}:location" for bid in bus_ids]
            else:
                keys = await redis.keys("bus:*:location")

            if keys:
                raw_items = await redis.mget(keys)
                for raw in raw_items:
                    if not raw:
                        continue
                    try:
                        data = json.loads(raw)
                        bus_obj = _build_bus_response(data, now)
                        if bus_obj:
                            if route_id and bus_obj.route_id != route_id:
                                continue
                            buses.append(bus_obj)
                    except json.JSONDecodeError:
                        continue

            if buses:
                return LiveBusListResponse(
                    total=len(buses),
                    timestamp=now,
                    buses=buses
                )
    except Exception as redis_err:
        logger.warning(f"Redis unavailable for GET /buses/live ({redis_err}). Falling back to PostGIS DB.")

    # 2. Fallback to PostGIS database
    if db is not None:
        try:
            subq = (
                select(GpsPoint.bus_id, func.max(GpsPoint.recorded_at).label("max_recorded"))
                .group_by(GpsPoint.bus_id)
            ).subquery()

            stmt = (
                select(GpsPoint)
                .join(subq, (GpsPoint.bus_id == subq.c.bus_id) & (GpsPoint.recorded_at == subq.c.max_recorded))
                .order_by(GpsPoint.recorded_at.desc())
            )

            res = await db.execute(stmt)
            points = res.scalars().all()

            for pt in points:
                pt_recorded = pt.recorded_at
                if pt_recorded.tzinfo is None:
                    pt_recorded = pt_recorded.replace(tzinfo=timezone.utc)
                seconds_since = max(0, int((now - pt_recorded).total_seconds()))

                bus_obj = LiveBusResponse(
                    bus_id=str(pt.bus_id),
                    registration_number=f"KA-25-{pt.bus_id}",
                    route_id=route_id or "route-001",
                    route_name="Live Route",
                    trip_id=str(pt.trip_id),
                    latitude=pt.latitude,
                    longitude=pt.longitude,
                    speed_kmh=round(pt.speed_mps * 3.6, 1),
                    heading=pt.heading,
                    last_updated=pt_recorded,
                    seconds_since_update=seconds_since,
                    status="in_transit",
                    occupancy_level="medium"
                )
                buses.append(bus_obj)

            if buses:
                return LiveBusListResponse(
                    total=len(buses),
                    timestamp=now,
                    buses=buses
                )
        except Exception as db_err:
            logger.warning(f"DB fallback failed for GET /buses/live ({db_err}). Falling back to demo data.")

    # 3. Fallback to demo data if both Redis and DB are unpopulated/unavailable
    demo_filtered = DEMO_LIVE_BUSES
    if route_id:
        demo_filtered = [b for b in DEMO_LIVE_BUSES if b.route_id == route_id]

    for b in demo_filtered:
        b.seconds_since_update = max(0, int((now - b.last_updated).total_seconds()))

    return LiveBusListResponse(
        total=len(demo_filtered),
        timestamp=now,
        buses=demo_filtered
    )
