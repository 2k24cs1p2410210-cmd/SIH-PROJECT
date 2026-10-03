# TransitPulse AI — Project Memory & Technical Blueprint

> **Permanent Source of Truth for TransitPulse AI Architecture, Implementation State, and Roadmap.**

---

## 📅 Last Updated
`2026-10-02 16:20:00 UTC`

---

## 🎯 1. Project Objective & Core Philosophy
TransitPulse AI is built to provide an affordable, resilient, AI-powered real-time public transit tracking and ETA prediction platform tailored for Tier-2 and Tier-3 Indian cities (e.g., Hubballi-Dharwad, Mysuru, Surat, Jaipur).

* **Zero-GTFS Requirement**: Operates independently without requiring official GTFS/GTFS-RT infrastructure.
* **Low-Cost Sensor Layer**: Uses Android smartphones carried by bus drivers as active GPS beacons emitting location fixes every 5–10 seconds.
* **Resilient GPS Ingestion**: Cleans noisy GPS data, removes spatial/temporal outliers, handles intermittent connectivity via offline SQLite/Room queue, and performs nearest-route map matching.
* **Multi-Tier Fallback ETA Engine**: Blends XGBoost trajectory models, historical segment averages, current speed baselines, and timetable schedules with real-time confidence scores.

---

## 🏗️ 2. Chosen Technology Stack

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Monorepo** | `pnpm` Workspaces | Efficient dependency sharing across Next.js apps & TypeScript packages. |
| **Passenger Web App** | Next.js 15 (App Router), Tailwind CSS, MapLibre GL JS, TanStack Query | Fast server side rendering, modern UI, open-source GIS map rendering. |
| **Admin Web App** | Next.js 15 (App Router), Tailwind CSS, MapLibre GL JS, Recharts | Real-time fleet overview, analytics, dispatch alerts. |
| **Driver App** | Native Android (Kotlin, Jetpack Compose, Room, WorkManager, Retrofit) | Reliable background location tracking and offline location caching. |
| **Backend API** | Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0 (asyncio) | Asynchronous performance, high-throughput geospatial ingestion, auto OpenAPI generation. |
| **Database** | PostgreSQL 16 + PostGIS 3.4 | Spatial queries (`ST_DWithin`, `ST_LineLocatePoint`, `ST_Distance`). |
| **Cache / Realtime** | Redis 7 (Pub/Sub & In-Memory Store) | High-speed vehicle location state caching and WebSocket broadcasting. |
| **ML Engine** | Python, pandas, scikit-learn, XGBoost | Baseline current speed & historical segment modeling with planned PyTorch LSTM upgrade. |

---

## 📐 3. Current Implementation Status

### Bootstrapped Infrastructure (Phase 1 Complete)
- [x] Monorepo root setup (`package.json`, `pnpm-workspace.yaml`, `docker-compose.yml`, `Makefile`, `.env.example`).
- [x] Complete documentation suite (`ARCHITECTURE.md`, `API_CONTRACT.md`, `DATABASE_SCHEMA.md`, `ETA_STRATEGY.md`, `GPS_PROCESSING.md`, `DEVELOPMENT_GUIDE.md`, `DEMO_GUIDE.md`, `CORE_FLOW_AUDIT.md`, `GPS_INGESTION_TEST.md`, `ADR-001`).
- [x] Shared TypeScript contracts (`packages/shared-types`).
- [x] Shared UI components (`packages/ui`).
- [x] Async FastAPI Backend with health, live buses, route, stop arrival, GPS update, and trip control endpoints with deterministic mock defaults.
- [x] PostGIS database schema definition and Alembic migration framework.
- [x] Plugable ETA Predictor baseline architecture (`CurrentSpeedPredictor`, `HistoricalAveragePredictor`, `MLModelPredictor` stub, `FallbackETAPredictor`).
- [x] Spatial Nearest-Route map matcher framework.
- [x] PostGIS GPS Point Persistence in `GpsIngestionService` for valid `POST /api/v1/gps/update` requests.
- [x] Passenger Web App with interactive MapLibre map placeholder, live bus list, ETA cards, and freshness indicators.
- [x] Admin Web App with fleet metrics summary, active bus status table, and route performance placeholders.
- [x] Driver Android App Kotlin/Compose project structure, location service architecture, and Room/WorkManager stubs.
- [x] Docker compose configuration for PostgreSQL/PostGIS, Redis, API, Passenger Web, and Admin Web.
- [x] End-to-end live tracking pipeline audit report ([`docs/CORE_FLOW_AUDIT.md`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/docs/CORE_FLOW_AUDIT.md)).
- [x] Manual verification guide for GPS ingestion persistence ([`docs/GPS_INGESTION_TEST.md`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/docs/GPS_INGESTION_TEST.md)).

---

## 📁 4. Initial Repository Structure

```
transit-pulse-ai/
├── README.md
├── LICENSE
├── .gitignore
├── .editorconfig
├── .env.example
├── docker-compose.yml
├── pnpm-workspace.yaml
├── package.json
├── Makefile
├── docs/
│   ├── PROJECT_MEMORY.md
│   ├── CORE_FLOW_AUDIT.md
│   ├── GPS_INGESTION_TEST.md
│   ├── ARCHITECTURE.md
│   ├── API_CONTRACT.md
│   ├── DATABASE_SCHEMA.md
│   ├── ETA_STRATEGY.md
│   ├── GPS_PROCESSING.md
│   ├── DEVELOPMENT_GUIDE.md
│   ├── DEMO_GUIDE.md
│   └── decisions/
│       └── ADR-001-monorepo-and-stack.md
├── apps/
│   ├── passenger-web/
│   ├── admin-web/
│   └── driver-android/
├── services/
│   ├── api/
│   └── ml/
├── packages/
│   ├── shared-types/
│   ├── ui/
│   └── config/
├── infrastructure/
│   ├── docker/
│   ├── github/
│   └── monitoring/
├── scripts/
└── sample-data/
```

---

## 🔄 5. Change Log

### `2026-10-02 16:20:00 UTC` — Backend PostGIS GPS Ingestion Persistence Gap Implementation
* **Implemented**: Integrated database persistence for accepted valid GPS points in `GpsIngestionService` (`POST /api/v1/gps/update`), adding PostGIS SRID 4326 geometry point generation, safe transaction rollback handling, backward-compatible API response counts (`accepted_count`, `rejected_count`, `persisted_count`), and full test coverage.
* **Files Modified**:
  * [`services/api/app/schemas/gps.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/schemas/gps.py) (Added `accepted_count`, `rejected_count`, `persisted_count` to `GpsUpdateResponse`)
  * [`services/api/app/repositories/gps_repository.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/repositories/gps_repository.py) (Added `add_points` batch method & explicit transaction rollback error handling)
  * [`services/api/app/services/gps_ingestion_service.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/services/gps_ingestion_service.py) (Added `WKTElement` PostGIS SRID 4326 geometry creation, UUID parsing, and `GpsRepository` invocation)
  * [`services/api/app/api/v1/gps.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/app/api/v1/gps.py) (Injected `AsyncSession` dependency & HTTP 500 exception handling)
  * [`services/api/pyproject.toml`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/pyproject.toml) (Configured setuptools package discovery and added `email-validator`)
  * [`services/api/tests/conftest.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/tests/conftest.py) (Updated HTTPX `ASGITransport` initialization)
  * [`docs/PROJECT_MEMORY.md`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/docs/PROJECT_MEMORY.md) (Updated)
* **Files Created**:
  * [`services/api/tests/gps/test_gps_ingestion.py`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/services/api/tests/gps/test_gps_ingestion.py) (Unit/Integration test suite covering valid persistence with SRID 4326, invalid rejection, and DB error rollback)
  * [`docs/GPS_INGESTION_TEST.md`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/docs/GPS_INGESTION_TEST.md) (Manual verification guide)
* **Migration Details**: Preserved existing `GpsPoint` SQLAlchemy model schema mapping to `gps_points` table with PostGIS SRID 4326 point geometry column.
* **Testing Performed & Commands**:
  * `services/api/.venv/Scripts/python -m pytest services/api/tests` (9 unit/integration tests passed in 4.34s)
* **Known Issues**:
  * `GET /api/v1/buses/live` currently returns static `DEMO_LIVE_BUSES` until Redis caching is connected.
* **Recommended Next Task**: Implement Redis caching for live bus positions in `GpsIngestionService` and connect `GET /api/v1/buses/live` to query active bus states from Redis.

### `2026-10-02 15:45:00 UTC` — End-to-End Live Tracking Pipeline Audit
* **Implemented**: Performed focused audit of the 10-point live driver-to-passenger tracking pipeline across Android app, FastAPI backend, and Next.js web client. Produced [`docs/CORE_FLOW_AUDIT.md`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/docs/CORE_FLOW_AUDIT.md).
* **Files Modified / Created**:
  * [`docs/CORE_FLOW_AUDIT.md`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/docs/CORE_FLOW_AUDIT.md) (Created)
  * [`docs/PROJECT_MEMORY.md`](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/docs/PROJECT_MEMORY.md) (Updated)
* **Audit Summary**:
  * Functional (1/10): Item 7 (WebSocket backend broadcast)
  * Partial / Disconnected (5/10): Item 2 (Android location tracker), Item 3 (Android sync worker), Item 4 (Backend cleaner/matcher), Item 8 (Passenger React Query polling), Item 10 (Data freshness badge)
  * Mocked (3/10): Item 1 (Android start trip button), Item 6 (Backend live buses static list), Item 9 (Passenger map CSS mock layout)
  * Missing (1/10): Item 5 (Backend Redis bus location cache)
* **Recommended Next Task**: Connect Backend DB/Redis persistence in `GpsIngestionService` and replace static `DEMO_LIVE_BUSES` in `GET /api/v1/buses/live`.

### `2026-09-27 23:17:00 UTC` — High-Level Architecture Diagram & MVP Definition Synchronization
* **Implemented**: Integrated high-level simplified system diagram (`Driver App → Backend API → Database/Redis → Passenger Web App / Admin Dashboard`) and explicit 5-point MVP execution flow across documentation files.
* **Files Modified**:
  * [README.md](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/README.md)
  * [docs/ARCHITECTURE.md](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/docs/ARCHITECTURE.md)
  * [docs/PROJECT_MEMORY.md](file:///c:/Users/ASUS/OneDrive/Desktop/SIH-Project/docs/PROJECT_MEMORY.md)
* **Architecture Decisions**: Maintained simplified single diagram structure alongside detailed component flow diagram.
* **APIs / Schema / Environment Changes**: None. All existing API contracts and PostGIS schemas preserved.
* **Testing Performed**: Python syntax compilation check (`python -m compileall`) verified 100% clean compilation.
* **Known Issues**: None introduced.
* **Recommended Next Task**: Implement the real driver GPS ingestion flow end-to-end: Android app → `POST /gps/update` → PostgreSQL/PostGIS → passenger live-map update.

### `2026-09-27 22:15:00 UTC` — Initial Repository Bootstrap

* **Implemented**: Project scaffolding, monorepo setup, full backend async API scaffold, database schemas, ETA engine baseline, map matcher stubs, Next.js web applications, Android Kotlin driver scaffold, seed scripts, and Docker integration.
* **Files Created**:
  * Top-level configuration (`README.md`, `LICENSE`, `.gitignore`, `.editorconfig`, `.env.example`, `docker-compose.yml`, `pnpm-workspace.yaml`, `package.json`, `Makefile`).
  * Architectural documentation in `docs/`.
  * `packages/shared-types`, `packages/ui`, `packages/config`.
  * `services/api`: FastAPI app, Pydantic schemas, SQLAlchemy models, Alembic configuration, ETA predictors, GPS processing, map matchers, seed scripts, pytest test suite.
  * `services/ml`: ML trajectory pipeline framework, synthetic GPS data generator scripts, XGBoost/LSTM placeholders.
  * `apps/passenger-web`: Next.js 15 App router structure, MapLibre GL map component, ETACard, ConfidenceBadge, live buses query.
  * `apps/admin-web`: Next.js 15 App router structure, Fleet overview summary, active buses table, route performance chart placeholder.
  * `apps/driver-android`: Android Kotlin project with Compose UI screens (Login, TripControl, LocationStatus), Room database DAO/Entities, WorkManager worker, Location foreground service.
  * `infrastructure/`: PostGIS init SQL, Nginx sample config, GitHub Actions workflows.
  * `scripts/`: Shell setup & maintenance scripts.
  * `sample-data/`: GeoJSON demo routes and stop sequences.
* **APIs Added**:
  * `GET /api/v1/health`
  * `GET /api/v1/buses/live`
  * `GET /api/v1/routes`
  * `GET /api/v1/stops/{stop_id}/arrivals`
  * `POST /api/v1/gps/update`
  * `POST /api/v1/trips/start`
  * `POST /api/v1/trips/end`
  * `WS /api/v1/ws/live`
* **Database Tables Created**:
  * `users`, `drivers`, `buses`, `routes`, `stops`, `trips`, `gps_points`, `predictions`, `alerts`, `incidents`.
* **Environment Variables**:
  * `DATABASE_URL`, `REDIS_URL`, `API_PORT`, `JWT_SECRET`, `NEXT_PUBLIC_API_BASE_URL`, `NEXT_PUBLIC_WS_BASE_URL`.

---

## 🏃 6. Commands to Run & Test

```bash
# 1. Monorepo Setup & Install
pnpm install

# 2. Local Backend Run (Python)
cd services/api
pip install -e .
python scripts/seed_demo_data.py
uvicorn app.main:app --reload --port 8000

# 3. Local Web Apps Run (Frontend)
pnpm dev

# 4. Tests
pnpm test
cd services/api && pytest

# 5. Full Docker Stack
docker-compose up -d
```

---

## ⚠️ 7. Known Issues, Shortcuts & Assumptions
* **Mock Data**: DB endpoints fallback to deterministic demo data when PostgreSQL connection is unavailable locally.
* **Valhalla Map Matcher**: Stubbed as placeholder adapter; `NearestRouteMapMatcher` is used as primary MVP matcher.
* **Authentication**: Scaffolding provided via JWT headers, but full auth check is bypassable in demo mode for frictionless testing.

---

## 🚀 8. Recommended Next Implementation Step
> **Implement Redis location state caching in `GpsIngestionService` and wire `GET /api/v1/buses/live` to return live active bus states from Redis instead of static `DEMO_LIVE_BUSES`.**
