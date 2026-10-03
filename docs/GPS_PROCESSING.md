# TransitPulse AI — GPS Processing Pipeline

## Pipeline Overview

```
[ Raw GPS Fix from Driver Phone ]
               │
               ▼
      ( 1. Coordinate Validation )
       - Lat: [-90, 90], Lon: [-180, 180]
       - Accuracy <= 50m
               │
               ▼
      ( 2. Temporal & Duplicate Filter )
       - Reject points with timestamp <= previous point
       - Ignore duplicate location fixes within 1 second
               │
               ▼
      ( 3. Speed & Jitter Outlier Detection )
       - Calculate speed = Distance / DeltaT
       - Reject jumps where speed > 120 km/h (33.3 m/s)
               │
               ▼
      ( 4. Nearest-Route Map Matcher )
       - Find active route geometry in PostGIS
       - Project GPS point onto nearest segment (ST_LineLocatePoint)
       - Compute cumulative route progress distance in meters
               │
               ▼
      ( 5. Store Cleaned Point & Publish Live Event )
```

---

## Processing Rules & Constants

| Check | Threshold | Action on Violation |
| :--- | :--- | :--- |
| **Accuracy** | $> 50.0\text{ meters}$ | Drop location point, log warning. |
| **Max Speed Jump** | $> 120.0\text{ km/h}$ | Drop location point as GPS teleport jitter. |
| **Min Speed** | $< 1.0\text{ km/h}$ | Classify bus as "stopped at signal/traffic/stop". |
| **Freshness Expiry** | $> 120.0\text{ seconds}$ | Flag vehicle state as "stale/signal lost". |
| **Max Off-Route Distance**| $> 200.0\text{ meters}$ | Trigger route deviation alert on Admin dashboard. |
