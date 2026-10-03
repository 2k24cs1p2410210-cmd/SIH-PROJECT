import json
import logging
import uuid
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.elements import WKTElement
from app.core.config import settings
from app.core.redis import get_redis
from app.schemas.gps import GpsUpdateInput, GpsUpdateResponse
from app.gps.cleaner import GPSCleaner
from app.mapping.nearest_route_matcher import NearestRouteMapMatcher
from app.services.websocket_manager import websocket_manager
from app.models.gps_point import GpsPoint
from app.repositories.gps_repository import GpsRepository

logger = logging.getLogger(__name__)


def _parse_uuid(val: str) -> uuid.UUID:
    try:
        return uuid.UUID(val)
    except ValueError:
        return uuid.uuid5(uuid.NAMESPACE_DNS, str(val))


class GpsIngestionService:
    def __init__(self):
        self.cleaner = GPSCleaner()
        self.matcher = NearestRouteMapMatcher()

    async def process_gps_update(
        self,
        input_data: GpsUpdateInput,
        db: Optional[AsyncSession] = None
    ) -> GpsUpdateResponse:
        # 1. Clean point
        is_clean = self.cleaner.clean_point(
            input_data.latitude,
            input_data.longitude,
            input_data.accuracy_m,
            input_data.speed_mps
        )

        if not is_clean:
            logger.warning(f"GPS point rejected for trip {input_data.trip_id} (noisy fix)")
            return GpsUpdateResponse(
                status="rejected",
                is_processed=False,
                accepted_count=0,
                rejected_count=1,
                persisted_count=0
            )

        # 2. Map Match point
        matched_lat, matched_lon, progress_m = self.matcher.match_point(
            input_data.latitude, input_data.longitude, "route-001"
        )

        # 3. Persist valid GPS point to PostgreSQL/PostGIS if DB session provided
        point_id: Optional[int] = None
        persisted_count = 0

        if db is not None:
            wkt_geom = WKTElement(f"POINT({input_data.longitude} {input_data.latitude})", srid=4326)
            gps_point = GpsPoint(
                trip_id=_parse_uuid(input_data.trip_id),
                bus_id=_parse_uuid(input_data.bus_id),
                latitude=input_data.latitude,
                longitude=input_data.longitude,
                geometry=wkt_geom,
                speed_mps=input_data.speed_mps,
                heading=input_data.heading,
                accuracy_m=input_data.accuracy_m,
                recorded_at=input_data.recorded_at,
                matched_distance_m=progress_m
            )
            repo = GpsRepository(db)
            saved_point = await repo.add_point(gps_point)
            point_id = saved_point.id
            persisted_count = 1

        # 3.5 Write live location to Redis cache
        route_id = getattr(input_data, "route_id", None) or "route-001"
        try:
            redis = await get_redis()
            if redis is not None:
                redis_key = f"bus:{input_data.bus_id}:location"
                location_data = {
                    "lat": matched_lat,
                    "lon": matched_lon,
                    "speed": input_data.speed_mps,
                    "bearing": input_data.heading,
                    "timestamp": input_data.recorded_at.isoformat(),
                    "trip_id": input_data.trip_id,
                    "route_id": route_id,
                    "bus_id": input_data.bus_id
                }
                ttl = getattr(settings, "REDIS_BUS_LOCATION_TTL", 120)
                await redis.set(redis_key, json.dumps(location_data), ex=ttl)
                await redis.sadd(f"route:{route_id}:buses", input_data.bus_id)
        except Exception as redis_exc:
            logger.warning(f"Redis write failure for bus {input_data.bus_id}: {redis_exc}")

        # 4. Broadcast update to WebSockets
        event_payload = {
            "event": "bus_location_update",
            "data": {
                "bus_id": input_data.bus_id,
                "trip_id": input_data.trip_id,
                "latitude": matched_lat,
                "longitude": matched_lon,
                "speed_kmh": round(input_data.speed_mps * 3.6, 1),
                "heading": input_data.heading,
                "recorded_at": input_data.recorded_at.isoformat()
            }
        }
        await websocket_manager.broadcast(event_payload)

        return GpsUpdateResponse(
            status="success",
            point_id=point_id or 1,
            is_processed=True,
            route_distance_m=progress_m,
            eta_updated=True,
            accepted_count=1,
            rejected_count=0,
            persisted_count=persisted_count
        )


gps_ingestion_service = GpsIngestionService()

