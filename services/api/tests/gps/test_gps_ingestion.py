import pytest
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.gps import GpsUpdateInput
from app.models.gps_point import GpsPoint
from app.services.gps_ingestion_service import GpsIngestionService
from app.repositories.gps_repository import GpsRepository


@pytest.mark.asyncio
async def test_valid_gps_point_persists_row_with_srid_4326():
    """Test 1 & 2: Valid GPS point creates database row with SRID 4326 geometry."""
    mock_db = AsyncMock(spec=AsyncSession)
    service = GpsIngestionService()

    input_data = GpsUpdateInput(
        trip_id="550e8400-e29b-41d4-a716-446655440000",
        bus_id="bus-101",
        latitude=15.364708,
        longitude=75.123955,
        speed_mps=8.5,
        heading=120.0,
        accuracy_m=5.0,
        recorded_at=datetime.now(timezone.utc)
    )

    response = await service.process_gps_update(input_data, db=mock_db)

    assert response.status == "success"
    assert response.is_processed is True
    assert response.accepted_count == 1
    assert response.rejected_count == 0
    assert response.persisted_count == 1

    # Verify mock_db session calls
    mock_db.add.assert_called_once()
    added_point: GpsPoint = mock_db.add.call_args[0][0]

    assert isinstance(added_point, GpsPoint)
    assert added_point.latitude == 15.364708
    assert added_point.longitude == 75.123955
    assert added_point.speed_mps == 8.5
    assert added_point.accuracy_m == 5.0
    assert added_point.geometry is not None
    # WKTElement string representation includes SRID=4326; POINT(75.123955 15.364708)
    assert "4326" in str(added_point.geometry.srid) if hasattr(added_point.geometry, "srid") else "4326" in str(added_point.geometry)
    assert "75.123955" in str(added_point.geometry)
    assert "15.364708" in str(added_point.geometry)


@pytest.mark.asyncio
async def test_invalid_gps_point_rejected_and_not_persisted():
    """Test 3: Invalid/noisy GPS point (e.g. accuracy > 100m) is rejected and not persisted."""
    mock_db = AsyncMock(spec=AsyncSession)
    service = GpsIngestionService()

    input_data = GpsUpdateInput(
        trip_id="550e8400-e29b-41d4-a716-446655440000",
        bus_id="bus-101",
        latitude=15.364708,
        longitude=75.123955,
        speed_mps=8.5,
        heading=120.0,
        accuracy_m=250.0,  # Invalid accuracy > 100m limit
        recorded_at=datetime.now(timezone.utc)
    )

    response = await service.process_gps_update(input_data, db=mock_db)

    assert response.status == "rejected"
    assert response.is_processed is False
    assert response.accepted_count == 0
    assert response.rejected_count == 1
    assert response.persisted_count == 0

    # Ensure DB add and commit were NEVER called for rejected point
    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()


@pytest.mark.asyncio
async def test_database_failure_raises_exception_and_rolls_back():
    """Test 4: Database commit failure rolls back and raises error without claiming success."""
    mock_db = AsyncMock(spec=AsyncSession)
    mock_db.commit.side_effect = RuntimeError("Database connection lost")

    service = GpsIngestionService()

    input_data = GpsUpdateInput(
        trip_id="550e8400-e29b-41d4-a716-446655440000",
        bus_id="bus-101",
        latitude=15.364708,
        longitude=75.123955,
        speed_mps=8.5,
        heading=120.0,
        accuracy_m=5.0,
        recorded_at=datetime.now(timezone.utc)
    )

    with pytest.raises(RuntimeError, match="Database connection lost"):
        await service.process_gps_update(input_data, db=mock_db)

    # Verify rollback was called
    mock_db.rollback.assert_called_once()
