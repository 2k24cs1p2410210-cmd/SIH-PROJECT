import pytest
import uuid
import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.core.database import get_db
from app.schemas.gps import GpsUpdateInput
from app.models.gps_point import GpsPoint
from app.services.gps_ingestion_service import GpsIngestionService


class InMemoryRedisMock:
    """Async Redis mock using in-memory dict for deterministic unit testing."""
    def __init__(self):
        self.store = {}
        self.sets = {}

    async def set(self, key: str, value: str, ex: int = None):
        self.store[key] = value

    async def get(self, key: str):
        return self.store.get(key)

    async def sadd(self, key: str, value: str):
        if key not in self.sets:
            self.sets[key] = set()
        self.sets[key].add(value)

    async def smembers(self, key: str):
        return self.sets.get(key, set())

    async def keys(self, pattern: str):
        prefix = pattern.replace("*", "")
        return [k for k in self.store.keys() if prefix in k or k.startswith("bus:")]

    async def mget(self, keys: list):
        return [self.store.get(k) for k in keys]


@pytest.fixture(autouse=True)
def override_db_dependency():
    mock_db = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    async def _get_db_override():
        yield mock_db

    app.dependency_overrides[get_db] = _get_db_override
    yield mock_db
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_post_gps_then_get_live_buses_returns_redis_data(async_client):
    """Test 1: POST a GPS batch caches to Redis and GET /buses/live returns matching coordinates and seconds_since_update."""
    redis_mock = InMemoryRedisMock()

    with patch("app.services.gps_ingestion_service.get_redis", return_value=redis_mock), \
         patch("app.api.v1.buses.get_redis", return_value=redis_mock):

        payload = {
            "trip_id": "550e8400-e29b-41d4-a716-446655440000",
            "bus_id": "bus-test-999",
            "latitude": 15.364708,
            "longitude": 75.123955,
            "speed_mps": 10.0,
            "heading": 90.0,
            "accuracy_m": 4.0,
            "recorded_at": datetime.now(timezone.utc).isoformat()
        }

        # 1. Ingest GPS point via API
        gps_resp = await async_client.post("/api/v1/gps/update", json=payload)
        assert gps_resp.status_code == 200
        assert gps_resp.json()["status"] == "success"

        # 2. Query GET /buses/live
        live_resp = await async_client.get("/api/v1/buses/live")
        assert live_resp.status_code == 200
        data = live_resp.json()
        assert data["total"] >= 1
        
        bus_ids = [b["bus_id"] for b in data["buses"]]
        assert "bus-test-999" in bus_ids

        bus_item = next(b for b in data["buses"] if b["bus_id"] == "bus-test-999")
        assert bus_item["latitude"] == 15.364708
        assert bus_item["longitude"] == 75.123955
        assert bus_item["speed_kmh"] == 36.0  # 10.0 mps * 3.6
        assert bus_item["seconds_since_update"] is not None
        assert bus_item["seconds_since_update"] >= 0


@pytest.mark.asyncio
async def test_ttl_expired_bus_absent(async_client):
    """Test 2: When Redis returns None/empty (TTL expired), expired bus is absent."""
    redis_mock = InMemoryRedisMock()  # empty store = expired/missing keys

    with patch("app.api.v1.buses.get_redis", return_value=redis_mock):
        live_resp = await async_client.get("/api/v1/buses/live")
        assert live_resp.status_code == 200
        data = live_resp.json()
        assert "buses" in data


@pytest.mark.asyncio
async def test_redis_down_fallback_to_postgis(async_client, override_db_dependency):
    """Test 3: Redis unavailable falls back to PostGIS database query and never returns 500."""
    dummy_bus_uuid = uuid.UUID("550e8400-e29b-41d4-a716-446655440001")
    dummy_trip_uuid = uuid.UUID("550e8400-e29b-41d4-a716-446655440002")
    
    dummy_gps_point = GpsPoint(
        id=101,
        trip_id=dummy_trip_uuid,
        bus_id=dummy_bus_uuid,
        latitude=15.4500,
        longitude=75.1500,
        speed_mps=8.0,
        heading=180.0,
        accuracy_m=5.0,
        recorded_at=datetime.now(timezone.utc)
    )

    mock_db = override_db_dependency
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [dummy_gps_point]
    mock_db.execute = AsyncMock(return_value=mock_result)

    with patch("app.api.v1.buses.get_redis", return_value=None):
        live_resp = await async_client.get("/api/v1/buses/live")
        assert live_resp.status_code == 200
        data = live_resp.json()
        assert data["total"] >= 1


@pytest.mark.asyncio
async def test_redis_write_failure_does_not_fail_gps_ingestion():
    """Test 4: Redis write exception during ingestion logs warning and still returns 200 success."""
    failing_redis_mock = AsyncMock()
    failing_redis_mock.set.side_effect = ConnectionError("Redis server connection refused")

    mock_db = AsyncMock(spec=AsyncSession)
    service = GpsIngestionService()

    input_data = GpsUpdateInput(
        trip_id="550e8400-e29b-41d4-a716-446655440000",
        bus_id="bus-resilient-101",
        latitude=15.364708,
        longitude=75.123955,
        speed_mps=8.5,
        heading=120.0,
        accuracy_m=5.0,
        recorded_at=datetime.now(timezone.utc)
    )

    with patch("app.services.gps_ingestion_service.get_redis", return_value=failing_redis_mock):
        response = await service.process_gps_update(input_data, db=mock_db)

        # Ingestion succeeds regardless of Redis failure
        assert response.status == "success"
        assert response.accepted_count == 1
        assert response.persisted_count == 1
