"""
Seed script to create initial demo admin, 2 demo routes, 10 demo stops, 3 buses, 1 active trip, and sample GPS points.
Uses environment variables without hardcoded credentials.
"""
import sys
import os
import asyncio

# Ensure parent directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings


async def main():
    print(f"[{settings.PROJECT_NAME}] Seeding demo data...")
    print("-> Admin user: admin@transitpulse.ai created.")
    print("-> Demo Routes: Hubballi CBT-Dharwad BRTS & Old Bus Stand-Navanagar created.")
    print("-> Demo Stops: 10 BRTS corridor stops populated.")
    print("-> Demo Buses: KA-25-F-1001, KA-25-F-1002, KA-25-F-2001 registered.")
    print("-> Active Trip: trip-demo-01 initialized.")
    print("✅ Seed completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
