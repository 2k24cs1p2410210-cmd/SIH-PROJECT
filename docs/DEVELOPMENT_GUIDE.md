# TransitPulse AI — Local Development Guide

## Environment Prerequisites
- **Node.js**: `v20.x` or higher
- **pnpm**: `v9.x`
- **Python**: `3.12+`
- **PostgreSQL**: `16` with PostGIS extension (or Docker Compose)
- **Redis**: `7.x` (or Docker Compose)

---

## 1. Setting Up Monorepo

```bash
# Install workspace JS/TS packages
pnpm install

# Copy environment file templates
cp .env.example .env
cp services/api/.env.example services/api/.env
```

---

## 2. Python API Setup

```bash
cd services/api
python -m venv .venv

# Activate venv:
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate

pip install -e .

# Run demo seed script
python scripts/seed_demo_data.py

# Run unit & API tests
pytest

# Start dev server
uvicorn app.main:app --reload --port 8000
```

---

## 3. Frontend Web Apps Setup

```bash
# Start both Passenger & Admin apps concurrently
pnpm dev

# Or run specific apps:
pnpm dev:passenger   # Running on http://localhost:3000
pnpm dev:admin       # Running on http://localhost:3001
```

---

## 4. Running Docker Stack

```bash
# Launch PostgreSQL+PostGIS, Redis, API, Passenger Web, Admin Web
make up

# View real-time logs
make logs

# Stop stack
make down
```
