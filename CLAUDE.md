# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure Overview

The application is organized in a modular monolith with clear separation:

- `app/main.py`: Entry point with FastAPI app creation
- `app/api/router.py`: REST router endpoints
- `app/core`: Core utilities
- `app.db.session`: Database session management
- `app.modules.orders`: Complete order module with models, schemas, repository, service, routes
- `alembic`: Database migration tool
- `tests/unit`: Unit tests (SQLite in-memory)
- `tests/integration`: Integration tests (PostgreSQL)

## Key Development Commands

**Setup and Run**
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -e '.[dev]'

# Run fresh database
docker stop postgres-dev || true
docker rm postgres-dev || true
docker run -d \
  --name postgres-dev \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=app \
  -p 5432:5432 \
  postgres:15

# Run API in background
uvicorn app.main:app --reload &
```

**Testing**
```bash
pytest  # Uses in-memory SQLite, no database setup needed
```

**Database Migrations**
```bash
python -m alembic revision --autogenerate -m "init"
python -m alembic upgrade head
```

## Architecture Notes

- The project uses a feature-based modular structure
- `modules/orders` contains end-to-end functionality
- `repository.py` → database access layer
- `service.py` → business logic
- `routes.py` → API layer

This structure supports future evolution into microservices if needed.

## Current State

Branch: main
Commit: 45197bc (Initial commit)
Status: clean

## Next Steps

- CI (34935fb) - add CI to run UnitTests
- Authentication & authorization not yet implemented
- Order state transitions not yet implemented
