import sys
import os
import time
import argparse
import httpx
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def main():
    parser = argparse.ArgumentParser(description="Synthetic GPS Generator for live testing")
    parser.add_argument("--url", default="http://localhost:8000/api/v1/gps/update")
    parser.add_argument("--trip-id", default="trip-demo-01")
    parser.add_argument("--bus-id", default="KA-25-F-1001")
    parser.add_argument("--interval", type=int, default=5)
    args = parser.parse_args()

    # Route coordinates: Hubballi CBT to Dharwad BRTS segment
    waypoints = [
        (15.364708, 75.123955),
        (15.372000, 75.115000),
        (15.385000, 75.100000),
        (15.391200, 75.091500),
        (15.405000, 75.075000),
        (15.421500, 75.051200),
    ]

    print(f"🚀 Starting Synthetic GPS Generator for Trip '{args.trip_id}'...")
    print(f"Target API: {args.url} (Interval: {args.interval}s)")

    client = httpx.Client()

    for idx, (lat, lon) in enumerate(waypoints):
        payload = {
            "trip_id": args.trip_id,
            "bus_id": args.bus_id,
            "latitude": lat,
            "longitude": lon,
            "speed_mps": 9.5,
            "heading": 140.0,
            "accuracy_m": 3.5,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "battery_level": 92
        }

        try:
            resp = client.post(args.url, json=payload)
            print(f"[{idx+1}/{len(waypoints)}] Fix sent: ({lat:.5f}, {lon:.5f}) -> HTTP {resp.status_code}")
        except Exception as e:
            print(f"[{idx+1}/{len(waypoints)}] Failed to post GPS fix: {e}")

        time.sleep(args.interval)

    print("🏁 Synthetic GPS simulation complete!")


if __name__ == "__main__":
    main()
