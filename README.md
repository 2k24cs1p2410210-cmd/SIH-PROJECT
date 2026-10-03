# TransitPulse AI 🚌⚡

> **Affordable, deployable, AI-powered real-time public transport tracking & ETA prediction platform designed for small and medium Indian cities.**

TransitPulse AI works even when official GTFS or GTFS-Realtime feeds are unavailable. It uses low-cost Android smartphones carried by bus drivers as active GPS beacons and employs a hybrid ETA engine (Current Speed Baseline -> Historical Segment Averages -> XGBoost ML) to handle noisy GPS signals, missing data, and route deviations.

---

## 📐 Architecture Overview

```text
Driver App → Backend API → Database/Redis → Passenger Web App
                                       → Admin Dashboard
```

```
                      +-----------------------------+
                      |   Driver Android App        |
                      | (Kotlin, Compose, WorkMgr)  |
                      +--------------+--------------+
                                     |
                                     | HTTP POST (GPS 5-10s)
                                     v
+-------------------------------------------------------------------------+
|                              FastAPI Backend                            |
|                                                                         |
|  +--------------------+   +-----------------------+  +---------------+  |
|  |  GPS Ingestion     |-->| GPS Cleaning & Kalman |->| Route Matcher |  |
|  |  & Validation      |   | Outlier Removal       |  | (PostGIS)     |  |
|  +--------------------+   +-----------------------+  +-------+-------+  |
|                                                              |          |
|  +--------------------+   +-----------------------+          v          |
|  | Fallback ETA Engine|<--| Confidence Calculator |<---------+          |
|  | (Speed/Hist/ML)    |   | (Freshness/Accuracy)  |                     |
|  +---------+----------+   +-----------------------+                     |
|            |                                                            |
+------------|------------------------------------------------------------+
             |
             +--------------------+---------------------+
             | PostgreSQL/PostGIS | Redis PubSub / Cache|
             +---------+----------+----------+----------+
                       |                     |
                       v                     v WebSocket
             +-------------------+ +-------------------+
             | Passenger Web App | |  Admin Dashboard  |
             | (Next.js/MapLibre)| |(Next.js/Analytics)|
             +-------------------+ +-------------------+
```


---

## 🛠️ Tech Stack & Workspace Structure

Monorepo structured using **pnpm workspaces** & **Python**:

* **Apps**:
  * `apps/passenger-web`: Passenger live tracking & arrival estimates (Next.js 15, React 19, Tailwind CSS, MapLibre GL).
  * `apps/admin-web`: Operator & fleet dispatch dashboard (Next.js 15, Recharts, MapLibre GL).
  * `apps/driver-android`: Driver GPS beacon app (Kotlin, Jetpack Compose, FusedLocationProvider, Room, WorkManager).
* **Services**:
  * `services/api`: Async FastAPI backend, Pydantic v2, SQLAlchemy 2.0 (asyncio), PostGIS geospatial querying, Redis caching/WebSockets.
  * `services/ml`: Trajectory processing, baseline & XGBoost ETA model pipeline, synthetic GPS generator.
* **Packages**:
  * `packages/shared-types`: Shared TypeScript interfaces for API & WebSockets.
  * `packages/ui`: Shared React components (Buttons, Cards, Badges, EmptyStates).
  * `packages/config`: Centralized ESLint, TypeScript, and Prettier rules.

---

## ⚡ Quick Start

### Prerequisites
* **Node.js**: `v20.x` or higher
* **pnpm**: `v9.x` or higher (`npm i -g pnpm`)
* **Python**: `3.12+`
* **Docker & Docker Compose**: (Optional, for full stack with PostgreSQL/PostGIS & Redis)

### 1. Monorepo Setup

```bash
# Clone and install node dependencies
pnpm install

# Setup environment variables
cp .env.example .env
cp services/api/.env.example services/api/.env
```

### 2. Run API Backend (Local Python environment)

```bash
cd services/api
python -m venv .venv
# On Windows PowerShell: .venv\Scripts\Activate.ps1
# On Linux/macOS: source .venv/bin/activate
pip install -e .

# Seed demo data (buses, routes, stops, active trip)
python scripts/seed_demo_data.py

# Run FastAPI dev server
uvicorn app.main:app --reload --port 8000
```

### 3. Run Passenger & Admin Web Apps

```bash
# From workspace root
pnpm dev
```

* **Passenger App**: [http://localhost:3000](http://localhost:3000)
* **Admin Dashboard**: [http://localhost:3001](http://localhost:3001)
* **FastAPI OpenAPI Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Full Stack with Docker Compose

```bash
docker-compose up -d
```

---

## 📌 Features & MVP Scope

### Core MVP Workflow
1. Driver sends GPS coordinates (every 5-10 seconds).
2. Backend validates, cleans, and saves location updates in database/Redis cache.
3. Passenger can view real-time bus locations on an interactive live map.
4. Backend calculates basic ETA using distance, current speed, and segment history.
5. Passenger sees calculated ETA with real-time confidence scores and ranges.

* **Zero GTFS Requirement**: Works completely with custom spatial routes and stop sequences defined in PostGIS.
* **Resilient GPS Processing**: Dynamic speed bounds, coordinate validation, jitter cleaning, and nearest-route map matching.

* **Multi-Tier Fallback ETA Engine**:
  1. **ML Predictor** (XGBoost trajectory model when >50 historical trips exist)
  2. **Historical Segment Average** (Used when segment traversal history exists)
  3. **Current Speed Baseline** (Primary baseline: remaining distance / current speed)
  4. **Schedule Fallback** (Timetable based)
  5. **Low-Confidence State** (Clear indicator when signal lost)
* **Live WebSocket Broadcast**: Instant real-time map updates to passenger & admin web apps.

---

## 📑 Documentation

* [`docs/PROJECT_MEMORY.md`](docs/PROJECT_MEMORY.md) - Active state, decisions, and progress tracking.
* [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) - Deep dive system design & boundaries.
* [`docs/API_CONTRACT.md`](docs/API_CONTRACT.md) - REST endpoints & WebSocket JSON messages.
* [`docs/DATABASE_SCHEMA.md`](docs/DATABASE_SCHEMA.md) - PostGIS schema & index design.
* [`docs/ETA_STRATEGY.md`](docs/ETA_STRATEGY.md) - Predictor hierarchy & confidence scoring formulas.

---

## 📜 License
[MIT License](LICENSE)
