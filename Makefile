.PHONY: help build run stop test test-unit test-integration clean migrations

help:
	@echo "Available commands:"
	@echo "  build            - Build the docker images"
	@echo "  run              - Run the application (development with auto-reload, debug mode)"
	@echo "  stop             - Stop the application"
	@echo "  test             - Run all tests"
	@echo "  test-unit        - Run unit tests"
	@echo "  test-integration - Run integration tests with fresh database"
	@echo "  clean            - Clean up Docker containers and volumes"
	@echo "  migrations msg   - Generate alembic migration via Docker (e.g. make migrations msg='add cancelled status')"

build:
	docker compose build

run:
	docker compose up -d
	@echo "Application running at http://localhost:8000"
	@echo "Swagger UI is available at http://localhost:8000/docs"

stop:
	@echo "Stopping the application..."
	docker compose stop

test:
	$(MAKE) test-unit
	$(MAKE) test-integration

test-unit:
	@echo "Running unit tests..."
	docker run --rm --tty -e AUTH_JWT_SECRET_KEY=docker-unit-tests-key python-fastapi-example-oms-app:dev python -m pytest tests/unit/ -v

test-integration:
	$(MAKE) clean
	$(MAKE) run
	@echo "Running integration tests..."
	docker compose run --rm app python -m pytest tests/integration/ -v
	$(MAKE) clean

migrations:
	@if [ -z "$(msg)" ]; then echo "Usage: make migrations msg='your message'"; exit 1; fi
	docker compose run --rm app alembic revision --autogenerate -m "$(msg)"

clean:
	$(MAKE) stop
	@echo "Cleaning all data..."
	docker compose down -v
