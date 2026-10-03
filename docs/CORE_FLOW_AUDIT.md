# End-to-End Live Tracking Pipeline Audit — TransitPulse AI

> **Audit Date**: 2026-10-02  
> **Target Scope**: End-to-End Live Driver-to-Passenger Tracking Flow (Items 1–10)  
> **Objective**: Verify functional readiness of each component in the core pipeline against actual codebase implementation.

---

## Executive Summary Matrix

| # | Core Pipeline Item | Status | Key Affected Files |
|---|---|---|---|
| 1 | Android driver app can start a trip | **mocked** | [`TripControlScreen.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/ui/screens/TripControlScreen.kt), [`TripViewModel.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/viewmodel/TripViewModel.kt) |
| 2 | Android driver app can obtain physical device GPS | **partial** | [`LocationTracker.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/location/LocationTracker.kt), [`LocationForegroundService.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/location/LocationForegroundService.kt) |
| 3 | Android app can submit GPS to `POST /api/v1/gps/update` | **partial** | [`SyncGpsWorker.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/workers/SyncGpsWorker.kt), [`TransitApi.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/data/remote/TransitApi.kt) |
| 4 | Backend validates and persists GPS to PostgreSQL/PostGIS | **partial** | [`gps_ingestion_service.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/services/gps_ingestion_service.py), [`gps.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/api/v1/gps.py) |
| 5 | Backend updates latest bus location in Redis | **missing** | [`gps_ingestion_service.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/services/gps_ingestion_service.py) |
| 6 | `GET /api/v1/buses/live` reads latest positions correctly | **mocked** | [`buses.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/api/v1/buses.py) |
| 7 | WebSocket bus-location event is broadcast after GPS ingestion | **functional** | [`gps_ingestion_service.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/services/gps_ingestion_service.py), [`websocket_manager.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/services/websocket_manager.py) |
| 8 | Passenger app receives or polls the update | **partial** | [`useLiveBuses.ts`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/passenger-web/hooks/useLiveBuses.ts), [`LivePage`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/passenger-web/app/live/page.tsx) |
| 9 | Passenger map renders the changed bus position | **mocked** | [`TransitMap.tsx`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/passenger-web/components/map/TransitMap.tsx) |
| 10 | Data freshness and stale/offline states are displayed | **partial** | [`DataFreshnessIndicator.tsx`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/passenger-web/components/common/DataFreshnessIndicator.tsx), [`page.tsx`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/passenger-web/app/live/page.tsx) |

---

## Detailed Audit & Itemized Evidence

### Item 1: Android driver app can start a trip
* **Status**: `mocked`
* **Exact Evidence**:
  * In [`TripControlScreen.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/ui/screens/TripControlScreen.kt#L24-L38), the "START TRIP" button click handler only toggles local Compose UI variable `isTripActive = true`.
  * [`TripViewModel.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/viewmodel/TripViewModel.kt#L5-L8) is an un-invoked stub containing empty state parameters (`isTripActive`, `activeTripId`) with no functions.
  * Retrofit endpoint `startTrip` in [`TransitApi.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/data/remote/TransitApi.kt#L12) is never called.
  * Foreground service [`LocationForegroundService.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/location/LocationForegroundService.kt) is never launched via `Intent`.
* **Smallest Next Action**:
  * Wire button click in `TripControlScreen.kt` to call `TripViewModel.startTrip()`.
  * In `TripViewModel`, execute `TransitApi.startTrip()`, retrieve `trip_id`, and launch `LocationForegroundService` with `trip_id` and `bus_id` in Intent extras.

---

### Item 2: Android driver app can obtain physical device GPS
* **Status**: `partial`
* **Exact Evidence**:
  * [`LocationTracker.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/location/LocationTracker.kt#L12-L28) correctly wraps `FusedLocationProviderClient` and validates locations using `LocationValidator`.
  * However, [`LocationForegroundService.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/location/LocationForegroundService.kt#L13-L23) only creates a status bar notification and never instantiates or starts `LocationTracker`.
  * Permissions (`ACCESS_FINE_LOCATION`, `ACCESS_BACKGROUND_LOCATION`) are declared in [`AndroidManifest.xml`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/AndroidManifest.xml), but no runtime permission request flow exists in Compose UI.
* **Smallest Next Action**:
  * Add Compose runtime location permission requester in `TripControlScreen`.
  * Instantiate `LocationTracker` inside `LocationForegroundService` and register update listener on service start.

---

### Item 3: Android app can submit GPS to `POST /api/v1/gps/update`
* **Status**: `partial`
* **Exact Evidence**:
  * Retrofit network client interface in [`TransitApi.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/data/remote/TransitApi.kt#L9-L10) and offline background sync in [`SyncGpsWorker.kt`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/driver-android/app/src/main/java/com/transitpulse/driver/workers/SyncGpsWorker.kt#L21-L40) are written.
  * However, incoming GPS fixes received by `LocationTracker` are never saved into Room DB (`AppDatabase.gpsQueueDao()`), and `SyncGpsWorker` is never enqueued with `WorkManager`.
* **Smallest Next Action**:
  * In `LocationForegroundService`, write acquired `Location` updates directly into Room database (`GpsQueueEntity`).
  * Enqueue `SyncGpsWorker` using `WorkManager.enqueueUniquePeriodicWork` or trigger immediate Retrofit network call.

---

### Item 4: Backend validates and persists GPS to PostgreSQL/PostGIS
* **Status**: `partial`
* **Exact Evidence**:
  * [`GpsIngestionService.process_gps_update`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/services/gps_ingestion_service.py#L18-L32) validates accuracy & speed using `GPSCleaner` and computes nearest route projection using `NearestRouteMapMatcher`.
  * However, lines 49-55 construct and return `GpsUpdateResponse` without acquiring an async SQLAlchemy database session to save a `GPSPoint` record or update `trips`/`buses` tables in PostgreSQL/PostGIS.
* **Smallest Next Action**:
  * Update `process_gps_update` to take an async DB session parameter (`AsyncSession`), insert a `GPSPoint` record into PostgreSQL, and update `trip.last_location` / `bus.last_location`.

---

### Item 5: Backend updates latest bus location in Redis
* **Status**: `missing`
* **Exact Evidence**:
  * [`gps_ingestion_service.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/services/gps_ingestion_service.py) does not import or invoke Redis cache operations.
  * No Redis key setter (e.g. `bus:{bus_id}:location`) exists across `services/api/app/services/`.
* **Smallest Next Action**:
  * Add Redis client instance to `services/api/app/core/redis.py` and invoke `redis.hset(f"bus:{bus_id}:location", mapping=...)` inside `GpsIngestionService.process_gps_update`.

---

### Item 6: `GET /api/v1/buses/live` reads latest positions correctly
* **Status**: `mocked`
* **Exact Evidence**:
  * [`buses.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/api/v1/buses.py#L8-L65) defines static hardcoded dataset `DEMO_LIVE_BUSES` (3 bus items) and returns it unconditionally.
  * It does not query Redis cache or PostgreSQL/PostGIS database tables. Incoming `POST /api/v1/gps/update` requests have no effect on `GET /api/v1/buses/live`.
* **Smallest Next Action**:
  * Modify `get_live_buses` endpoint handler to scan Redis `bus:*:location` keys (or query active trips from PostGIS) and return actual dynamic bus states.

---

### Item 7: WebSocket bus-location event is broadcast after GPS ingestion
* **Status**: `functional`
* **Exact Evidence**:
  * [`gps_ingestion_service.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/services/gps_ingestion_service.py#L35-L47) constructs `"event": "bus_location_update"` payload with matched lat/lon and speed.
  * It calls `await websocket_manager.broadcast(event_payload)`, which iterates and sends JSON to all connected clients in [`websocket_manager.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/services/websocket_manager.py#L25-L33).
* **Smallest Next Action**:
  * Core backend trigger logic is functional. Ensure frontend WebSocket client connects to `/api/v1/ws/live` to consume these events.

---

### Item 8: Passenger app receives or polls the update
* **Status**: `partial`
* **Exact Evidence**:
  * [`useLiveBuses.ts`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/passenger-web/hooks/useLiveBuses.ts#L6-L10) polls `GET /api/v1/buses/live` every 10 seconds using `@tanstack/react-query`.
  * However, no WebSocket subscription hook exists in `apps/passenger-web/`, so real-time push updates from `WS /api/v1/ws/live` are not received. Polling receives static mock data due to Item 6.
* **Smallest Next Action**:
  * Implement `useWebSocket` hook in `apps/passenger-web/hooks/` listening on `/api/v1/ws/live` to invalidate or update the React Query `live-buses` cache immediately upon receiving `bus_location_update`.

---

### Item 9: Passenger map renders the changed bus position
* **Status**: `mocked`
* **Exact Evidence**:
  * [`TransitMap.tsx`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/passenger-web/components/map/TransitMap.tsx#L46-L51) positions bus icons using static hardcoded CSS pixel strings: `positions = [{ left: '280px', top: '240px' }, { left: '600px', top: '210px' }, { left: '450px', top: '300px' }]`.
  * MapLibre GL JS instance is not instantiated, and `latitude`/`longitude` properties of incoming bus objects are ignored.
* **Smallest Next Action**:
  * Replace SVG/CSS mockup in `TransitMap.tsx` with MapLibre GL `maplibregl.Map` instance and dynamically update bus marker coordinates (`marker.setLngLat([bus.longitude, bus.latitude])`).

---

### Item 10: Data freshness and stale/offline states are displayed
* **Status**: `partial`
* **Exact Evidence**:
  * [`DataFreshnessIndicator.tsx`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/passenger-web/components/common/DataFreshnessIndicator.tsx#L3-L9) renders visual freshness status ("Live • Updated Xs ago" vs "Stale signal (Xs)").
  * However, [`LivePage`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/apps/passenger-web/app/live/page.tsx#L48) passes a hardcoded prop `<DataFreshnessIndicator lastUpdatedSec={8} />` instead of calculating the dynamic time delta between current time and `bus.last_updated`.
* **Smallest Next Action**:
  * Compute `lastUpdatedSec = Math.floor((Date.now() - new Date(bus.last_updated).getTime()) / 1000)` dynamically in `LivePage` and pass to `DataFreshnessIndicator`.

---

## Audit Conclusion & Next Steps Roadmap

The high-level architecture, contracts, schema models, and component UI layouts are well-established (~55% - 60% overall system completion). However, the **live tracking pipeline connectivity** across components is currently decoupled by mock data wrappers.

To achieve complete end-to-end live tracking functionality, follow the sequence below:
1. **Phase 1 (Backend Pipeline)**: Implement DB/Redis persistence in `GpsIngestionService` (Items 4, 5) and wire `GET /api/v1/buses/live` to Redis (Item 6).
2. **Phase 2 (Android App Pipeline)**: Connect Trip screen to service launch, permissions, and Room/WorkManager sync (Items 1, 2, 3).
3. **Phase 3 (Passenger Web Pipeline)**: Add WebSocket client hook, MapLibre lat/lon marker positioning, and dynamic freshness calculation (Items 8, 9, 10).
