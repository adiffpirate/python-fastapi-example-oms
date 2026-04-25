.PHONY: help run run-dev test-unit test-integration clean stop

help:
	@echo "Available commands:"
	@echo "  build            - Build the docker container"
	@echo "  run              - Run the application (development with auto-reload, debug mode)"
	@echo "  test-unit        - Run unit tests"
	@echo "  test-integration - Run integration tests with fresh database"
	@echo "  stop             - Stop the application"
	@echo "  clean            - Clean up Docker containers and volumes"

build:
	docker build -t python-fastapi-example-oms:dev .

run:
	$(MAKE) build
	docker compose up -d
	@echo "Waiting for database to be ready..."
	until nc -zv localhost 5432; do sleep 1; done
	@echo "Running migrations..."
	docker compose run --rm app python -m alembic upgrade head
	@echo "Application running at http://localhost:8000"
	@echo "Swagger UI is available at http://localhost:8000/docs"

stop:
	@echo "Stopping the application..."
	docker compose stop

test-unit:
	$(MAKE) build
	@echo "Running unit tests..."
	docker compose run --rm app python -m pytest tests/unit/ -v

test-integration:
	$(MAKE) clean
	$(MAKE) run
	@echo "Running integration tests..."
	docker compose run --rm app python -m pytest tests/integration/ -v
	$(MAKE) clean

clean:
	$(MAKE) stop
	@echo "Cleaning all data..."
	docker compose down -v
