# TransitPulse AI — Demo & Presentation Guide

## 🚀 Quick Demo Walkthrough

This guide walks through demonstrating TransitPulse AI to stakeholders or evaluators using pre-populated demo data.

---

## 1. Start System Services

```bash
# Option A: Run locally using Python API & pnpm
cd services/api && python scripts/seed_demo_data.py
uvicorn app.main:app --reload --port 8000 &
pnpm dev

# Option B: Run via Docker Compose
docker-compose up -d
```

---

## 2. Live Demo Script (Step-by-Step)

### Step 1: Passenger Live Tracking ([http://localhost:3000/live](http://localhost:3000/live))
- Open Passenger Web App.
- Observe active bus markers on the map (e.g. `KA-25-F-1001` on Hubballi-Dharwad BRTS line).
- Click on a bus to expand the live ETA card.
- Point out the **Confidence Badge** ("High 88%"), **Data Freshness Indicator** ("10s ago"), and calculated arrival time for upcoming stops.

### Step 2: Simulate Live Driver GPS Stream
- Open a terminal and run the synthetic GPS generator script:
  ```bash
  python services/api/scripts/generate_synthetic_gps.py --trip-id trip-demo-01 --speed 35
  ```
- Watch the vehicle icon move smoothly along the route polyline in real-time on the passenger map without requiring page refreshes!

### Step 3: Admin Fleet Overview ([http://localhost:3001](http://localhost:3001))
- Open Admin Dashboard.
- Show live fleet counts (Active: 3, Inactive: 1, On-Time Rate: 94%).
- Demonstrate route performance metrics and live active trip list.

---

## 3. Key Talking Points for Judges & Evaluators
1. **No GTFS Lock-in**: Works out of the box with custom spatial PostGIS routes & stop definitions.
2. **Resilience**: Operates reliably under noisy 3G/4G connectivity with driver app offline queuing.
3. **Smart ETA Engine**: Smoothly transitions from simple speed baseline to trained XGBoost ML as historical data accumulates.
