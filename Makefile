.PHONY: help up down logs seed test lint reset-db dev

help:
	@echo "TransitPulse AI - Command Helper"
	@echo "---------------------------------"
	@echo "make up        : Start all Docker services (PostgreSQL, Redis, API, Passenger Web, Admin Web)"
	@echo "make down      : Stop all Docker services"
	@echo "make logs      : View logs from Docker services"
	@echo "make seed      : Run demo data seed script on local Python API"
	@echo "make test      : Run tests for JS packages and Python API"
	@echo "make lint      : Run linters across workspace"
	@echo "make reset-db  : Reset local PostgreSQL database and re-apply migrations/seed"
	@echo "make dev       : Start local frontend development apps"

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

seed:
	cd services/api && python scripts/seed_demo_data.py

test:
	pnpm test
	cd services/api && pytest

lint:
	pnpm lint

reset-db:
	docker-compose exec -T postgres psql -U transitpulse -d transitpulse_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	cd services/api && alembic upgrade head && python scripts/seed_demo_data.py

dev:
	pnpm dev
