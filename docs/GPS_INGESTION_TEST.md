# GPS Ingestion Persistence Manual Verification Guide

> **Document Type**: Step-by-Step Testing Guide  
> **Feature Scope**: PostGIS GPS Point Persistence (`POST /api/v1/gps/update`)

---

## Prerequisites
- PostgreSQL with PostGIS extension running (or docker stack: `docker-compose up -d db redis`)
- Python 3.12+ virtual environment set up (`services/api/.venv`)

---

## Step-by-Step Verification Protocol

### Step 1: Start Database & API Services

```bash
# Option A: Local Docker stack (recommended)
docker-compose up -d db redis

# Option B: Run FastAPI backend dev server locally
cd services/api
.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### Step 2: Seed Initial Demo Data

```bash
cd services/api
python scripts/seed_demo_data.py
```

### Step 3: Identify Active Trip & Bus Parameters

Active demo trip parameters populated by seed:
- `trip_id`: `"trip-demo-01"` (or UUID `"550e8400-e29b-41d4-a716-446655440000"`)
- `bus_id`: `"bus-101"` (or UUID `"123e4567-e89b-12d3-a456-426614174000"`)

### Step 4: Submit a Valid GPS Update via HTTP POST

Using cURL / Postman / Python:

```bash
curl -X POST "http://localhost:8000/api/v1/gps/update" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": "550e8400-e29b-41d4-a716-446655440000",
    "bus_id": "123e4567-e89b-12d3-a456-426614174000",
    "latitude": 15.364708,
    "longitude": 75.123955,
    "speed_mps": 8.5,
    "heading": 142.0,
    "accuracy_m": 4.2,
    "recorded_at": "2026-10-02T15:45:00Z"
  }'
```

**Expected JSON Response**:
```json
{
  "status": "success",
  "point_id": 1,
  "is_processed": true,
  "route_distance_m": 120.5,
  "eta_updated": true,
  "accepted_count": 1,
  "rejected_count": 0,
  "persisted_count": 1
}
```

### Step 5: Query Database to Verify Record & PostGIS SRID 4326

Using `psql` or database client:

```sql
SELECT 
    id, 
    trip_id, 
    bus_id, 
    latitude, 
    longitude, 
    ST_AsText(geometry) AS wkt_geom, 
    ST_SRID(geometry) AS srid,
    speed_mps, 
    recorded_at
FROM gps_points
ORDER BY id DESC
LIMIT 1;
```

**Expected Verification Output**:
- `srid`: `4326`
- `wkt_geom`: `POINT(75.123955 15.364708)`
- `latitude`: `15.364708`, `longitude`: `75.123955`
- `speed_mps`: `8.5`
