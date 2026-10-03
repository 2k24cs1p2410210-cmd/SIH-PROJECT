# TransitPulse AI — Architecture Documentation

## System Topology & Data Flow

### High-Level Architecture
```text
Driver App → Backend API → Database/Redis → Passenger Web App
                                       → Admin Dashboard
```

### Detailed Component Flow
```
[ Android Driver App ] (Kotlin, WorkManager, FusedLocation)
         │
         │ POST /api/v1/gps/update (Every 5-10s or offline batch)
         ▼
[ FastAPI Backend ] 
   ├── 1. Ingestion & Validation (Coordinate check, time check)
   ├── 2. GPS Processing (Kalman / Jitter filter, speed bounds)
   ├── 3. Map Matcher (PostGIS ST_LineLocatePoint / Valhalla Adapter)
   ├── 4. ETA Engine Orchestrator (Speed -> Hist Avg -> XGBoost)
   └── 5. State Cache & Broadcaster (Redis & WebSockets)
         │                                   │
         ▼                                   ▼
[ PostgreSQL / PostGIS ]             [ Redis PubSub / Cache ]
(Persistent Trips/Points)            (Live Bus State / Channels)
                                             │
                                             ▼
                             [ Passenger & Admin Web Apps ]
                             (Next.js 15, MapLibre, React Query)
```

---

## 🎯 Target MVP Definition & Execution Flow

1. **Driver sends GPS**: The driver Android app transmits GPS location fixes every 5-10 seconds to `POST /api/v1/gps/update`.
2. **Backend saves it**: FastAPI validates coordinates, filters noise/teleport jumps, projects location onto nearest route linestring, and persists fixes to PostgreSQL/PostGIS & Redis cache.
3. **Passenger can see bus location**: Live bus coordinates are broadcast via WebSockets to the Passenger Web App (`/live`) and rendered on the MapLibre map.
4. **Backend calculates basic ETA**: The Fallback ETA engine calculates remaining segment distance and evaluates current speed / historical segment averages.
5. **Passenger sees ETA and confidence**: The Passenger Web App renders the calculated arrival estimate alongside a dynamic confidence badge (High/Medium/Low) and margin bounds.


---

## Component Responsibilities

### 1. Driver Android App
- Obtains location fixes via Android `FusedLocationProviderClient`.
- Validates location accuracy before posting (ignores accuracy > 50m).
- Uses `Room` database to store location fixes locally when offline.
- Uses `WorkManager` to batch upload stored location fixes when network reconnects.
- Foreground service with notification icon ensures OS does not kill background location collection.

### 2. FastAPI Backend
- **GPS Ingestion**: High-throughput REST endpoint validating JSON payloads.
- **GPS Processing**: Standardizes spatial coordinates, computes speed, filters anomalies (jumps > 120 km/h).
- **Spatial Map Matcher**: Matches raw GPS coordinate to closest segment on active route polyline using PostGIS `ST_LineLocatePoint` and `ST_Distance`.
- **ETA Engine**: Evaluates available historical trip data and selects best predictor (Current Speed vs Historical Segment Average vs XGBoost Model).
- **Redis Cache & WebSockets**: Pushes instant state updates to connected frontend clients via Redis Pub/Sub channels.

### 3. Data Store (PostgreSQL 16 + PostGIS 3.4)
- Stores spatial route geometries (`LINESTRING`), stop locations (`POINT`), trip logs, and raw GPS history.
- Spatial indexing using GIST (`USING GIST(geom)`) for sub-millisecond proximity queries.

### 4. Passenger & Admin Web Applications
- **Passenger Web**: Displays live bus positions, route paths, stop locations, ETA cards with confidence indicators, and data freshness metrics.
- **Admin Web**: Displays fleet status overview, active trip monitor, route performance metrics, and emergency alert dispatching.

---

## Non-MVP / Future Boundary
- **Self-hosted Valhalla / OSRM**: Supported via pluggable interface; fallback MVP uses PostGIS nearest point line matching.
- **Kafka / Distributed Streaming**: Replaced by lightweight Redis Pub/Sub for MVP simplicity.
- **Kubernetes**: Deployed with lightweight Docker Compose for MVP simplicity.
