from fastapi import APIRouter
from app.api.v1 import (
    health,
    buses,
    routes,
    stops,
    gps,
    trips,
    auth,
    alerts,
    incidents,
    websocket,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(buses.router, tags=["Buses"])
api_router.include_router(routes.router, tags=["Routes"])
api_router.include_router(stops.router, tags=["Stops & ETA"])
api_router.include_router(gps.router, tags=["GPS Ingestion"])
api_router.include_router(trips.router, tags=["Trips"])
api_router.include_router(auth.router, tags=["Authentication"])
api_router.include_router(alerts.router, tags=["Alerts"])
api_router.include_router(incidents.router, tags=["Incidents"])
api_router.include_router(websocket.router, tags=["Live WebSockets"])
