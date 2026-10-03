# TransitPulse AI — Database Schema & Index Design

PostgreSQL 16 + PostGIS 3.4 spatial database layout.

---

## Entity Relationship Summary

```
[users] ──< [drivers]
                │
                └──< [trips] >── [buses]
                      │     └── [routes] ──< [stops]
                      │
                      ├──< [gps_points]
                      ├──< [predictions]
                      └──< [incidents]
```

---

## 1. Tables Overview

### `users`
- `id`: UUID (PK)
- `email`: VARCHAR(255) UNIQUE, NOT NULL
- `password_hash`: VARCHAR(255), NOT NULL
- `role`: VARCHAR(50) (admin, dispatcher, driver, passenger)
- `created_at`: TIMESTAMPTZ

### `buses`
- `id`: UUID (PK)
- `bus_code`: VARCHAR(50) UNIQUE, NOT NULL (e.g., "bus-101")
- `registration_number`: VARCHAR(50) UNIQUE, NOT NULL (e.g., "KA-25-F-1001")
- `capacity`: INTEGER
- `status`: VARCHAR(50) (active, maintenance, inactive)
- `created_at`: TIMESTAMPTZ

### `routes`
- `id`: UUID (PK)
- `route_code`: VARCHAR(50) UNIQUE, NOT NULL (e.g., "R-101")
- `name`: VARCHAR(255), NOT NULL
- `origin_name`: VARCHAR(100)
- `destination_name`: VARCHAR(100)
- `geometry`: GEOMETRY(LINESTRING, 4326)
- `distance_meters`: DOUBLE PRECISION

### `stops`
- `id`: UUID (PK)
- `stop_code`: VARCHAR(50) UNIQUE
- `name`: VARCHAR(255), NOT NULL
- `geometry`: GEOMETRY(POINT, 4326)
- `sequence_order`: INTEGER
- `route_id`: UUID (FK -> routes.id)

### `trips`
- `id`: UUID (PK)
- `bus_id`: UUID (FK -> buses.id)
- `driver_id`: UUID (FK -> users.id)
- `route_id`: UUID (FK -> routes.id)
- `status`: VARCHAR(50) (scheduled, active, completed, cancelled)
- `start_time`: TIMESTAMPTZ
- `end_time`: TIMESTAMPTZ

### `gps_points`
- `id`: BIGSERIAL (PK)
- `trip_id`: UUID (FK -> trips.id)
- `bus_id`: UUID (FK -> buses.id)
- `geometry`: GEOMETRY(POINT, 4326), NOT NULL
- `latitude`: DOUBLE PRECISION
- `longitude`: DOUBLE PRECISION
- `speed_mps`: DOUBLE PRECISION
- `heading`: DOUBLE PRECISION
- `accuracy_m`: DOUBLE PRECISION
- `recorded_at`: TIMESTAMPTZ, NOT NULL
- `matched_distance_m`: DOUBLE PRECISION

### `predictions`
- `id`: BIGSERIAL (PK)
- `trip_id`: UUID (FK -> trips.id)
- `stop_id`: UUID (FK -> stops.id)
- `eta_seconds`: INTEGER, NOT NULL
- `confidence_score`: DOUBLE PRECISION
- `predictor_type`: VARCHAR(50)
- `predicted_at`: TIMESTAMPTZ, NOT NULL

---

## 2. Spatial & Compound Indexes

```sql
-- Spatial index on route geometries
CREATE INDEX idx_routes_geometry ON routes USING GIST (geometry);

-- Spatial index on stop locations
CREATE INDEX idx_stops_geometry ON stops USING GIST (geometry);

-- Spatial index on raw & matched GPS points
CREATE INDEX idx_gps_points_geometry ON gps_points USING GIST (geometry);

-- High throughput query indexes for active trip tracking
CREATE INDEX idx_gps_points_trip_time ON gps_points (trip_id, recorded_at DESC);
CREATE INDEX idx_predictions_trip_stop ON predictions (trip_id, stop_id, predicted_at DESC);
CREATE INDEX idx_trips_status ON trips (status) WHERE status = 'active';
```
