"""
Celery Task Queue placeholder for background ML training & trajectory batch processing.
Not required for initial local dev run.
"""
import os

CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
