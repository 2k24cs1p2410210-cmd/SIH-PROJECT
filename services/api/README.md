# TransitPulse AI — Backend API Service

FastAPI async backend service providing real-time GPS ingestion, spatial route matching, multi-tier ETA prediction, and WebSocket streaming.

## Features
- **Geospatial Processing**: PostGIS ST_LineLocatePoint spatial queries and coordinate cleaning.
- **Pluggable ETA Engine**: Fallback hierarchy from Current Speed Baseline to Historical Segment Averages and XGBoost.
- **Resilient Fallbacks**: Degrades gracefully to sample demo data if local PostgreSQL or Redis services are offline.
- **WebSocket Gateway**: Real-time position broadcasting for passenger and admin web apps.

## Running Locally

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\Activate.ps1 on Windows

# 2. Install dependencies
pip install -e .

# 3. Seed demo data
python scripts/seed_demo_data.py

# 4. Start Uvicorn
uvicorn app.main:app --reload --port 8000
```
