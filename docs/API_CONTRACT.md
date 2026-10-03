# TransitPulse AI — API & WebSocket Contract

All API responses use ISO 8601 UTC timestamps and standard JSON envelopes.

---

## 1. Health & System
`GET /api/v1/health`

**Response (200 OK):**
```json
{
  "status": "healthy",
  "environment": "development",
  "version": "0.1.0",
  "database": "connected",
  "redis": "connected",
  "timestamp": "2026-09-27T22:15:00Z"
}
```

---

## 2. GPS Ingestion (Driver App -> Backend)
`POST /api/v1/gps/update`

**Request Body:**
```json
{
  "trip_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "bus_id": "bus-KA-25-F-1234",
  "latitude": 15.364708,
  "longitude": 75.123955,
  "altitude": 670.5,
  "speed_mps": 8.5,
  "heading": 142.0,
  "accuracy_m": 4.2,
  "recorded_at": "2026-09-27T22:14:55Z",
  "battery_level": 88
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "point_id": 1042,
  "is_processed": true,
  "route_distance_m": 4250.0,
  "eta_updated": true
}
```

---

## 3. Live Buses (Frontend -> Backend)
`GET /api/v1/buses/live`

**Response (200 OK):**
```json
{
  "total": 3,
  "timestamp": "2026-09-27T22:15:00Z",
  "buses": [
    {
      "bus_id": "bus-101",
      "registration_number": "KA-25-F-1001",
      "route_id": "route-001",
      "route_name": "Hubballi CBT to Dharwad BRTS",
      "trip_id": "trip-demo-01",
      "latitude": 15.364708,
      "longitude": 75.123955,
      "speed_kmh": 30.6,
      "heading": 142.0,
      "last_updated": "2026-09-27T22:14:55Z",
      "seconds_since_update": 5,
      "status": "in_transit",
      "occupancy_level": "medium"
    }
  ]
}
```

---

## 4. Stop Arrivals & ETA
`GET /api/v1/stops/{stop_id}/arrivals`

**Response (200 OK):**
```json
{
  "stop_id": "stop-003",
  "stop_name": "Unkal Lake BRTS",
  "timestamp": "2026-09-27T22:15:00Z",
  "arrivals": [
    {
      "bus_id": "bus-101",
      "route_id": "route-001",
      "route_name": "Hubballi CBT to Dharwad BRTS",
      "eta_seconds": 340,
      "eta_timestamp": "2026-09-27T22:20:40Z",
      "confidence_score": 0.88,
      "confidence_level": "high",
      "range_min_seconds": 300,
      "range_max_seconds": 410,
      "predictor_type": "current_speed",
      "distance_remaining_m": 2450.0
    }
  ]
}
```

---

## 5. WebSockets Live Channel
`WS /api/v1/ws/live`

**Broadcast Message Payload:**
```json
{
  "event": "bus_location_update",
  "data": {
    "bus_id": "bus-101",
    "trip_id": "trip-demo-01",
    "route_id": "route-001",
    "latitude": 15.364708,
    "longitude": 75.123955,
    "speed_kmh": 30.6,
    "heading": 142.0,
    "recorded_at": "2026-09-27T22:14:55Z",
    "next_stop_id": "stop-003",
    "next_stop_eta_seconds": 340
  }
}
```
