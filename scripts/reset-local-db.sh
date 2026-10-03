#!/usr/bin/env bash
set -e
echo "Resetting PostgreSQL database..."
docker-compose exec -T postgres psql -U transitpulse -d transitpulse_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; CREATE EXTENSION IF NOT EXISTS postgis;"
cd services/api && alembic upgrade head && python scripts/seed_demo_data.py
echo "✅ Database reset complete!"
