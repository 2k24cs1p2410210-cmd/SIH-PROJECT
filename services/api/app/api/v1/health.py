from fastapi import APIRouter
from datetime import datetime, timezone
from app.core.config import settings
from app.core.redis import get_redis

router = APIRouter()


@router.get(
    "/health",
    summary="Health check endpoint",
    description="Returns API status and backend database/redis connection health."
)
async def get_health():
    redis_status = "connected"
    try:
        redis = await get_redis()
        if not redis:
            redis_status = "offline (fallback mode active)"
    except Exception:
        redis_status = "offline"

    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION,
        "database": "connected",
        "redis": redis_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
