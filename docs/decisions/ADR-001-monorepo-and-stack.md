# ADR-001: Monorepo Architecture & Core Tech Stack

* **Status**: Accepted
* **Date**: 2026-09-27
* **Context**: TransitPulse AI requires rapid iteration across frontend web apps, driver Android app, FastAPI backend, and ML data pipelines.

## Decision

1. **Repository Structure**:
   Use a monorepo managed via `pnpm` workspaces for frontend apps (`apps/passenger-web`, `apps/admin-web`) and TypeScript packages (`packages/shared-types`, `packages/ui`, `packages/config`).

2. **Backend Engine**:
   FastAPI with Python 3.12, async SQLAlchemy 2.0, PostgreSQL 16 + PostGIS 3.4 for spatial processing, and Redis 7 for real-time pub/sub and bus state caching.

3. **Driver Mobile App**:
   Native Android in Kotlin with Jetpack Compose, Room DB, WorkManager, and FusedLocationProvider for reliable low-power background location tracking.

4. **ETA Engine Fallback**:
   Implement pluggable ETA predictor hierarchy (Current Speed -> Historical Segment Average -> XGBoost ML -> Schedule) to operate out of the box without prior GTFS or historical datasets.

## Consequences

* **Pros**:
  * Unified codebase for fast multi-app development.
  * Zero GTFS dependency ensures deployment feasibility in small/medium cities.
  * Shared TypeScript types prevent contract drift between backend & frontend.
* **Cons**:
  * Requires managing both Node.js (pnpm) and Python (pip/pyproject) environments.
