.PHONY: help run stop test test-unit test-integration clean

help:
	@echo "Available commands:"
	@echo "  build            - Build the docker container"
	@echo "  run              - Run the application (development with auto-reload, debug mode)"
	@echo "  test             - Run all tests"
	@echo "  test-unit        - Run unit tests"
	@echo "  test-integration - Run integration tests with fresh database"
	@echo "  stop             - Stop the application"
	@echo "  clean            - Clean up Docker containers and volumes"

build:
	docker build -t python-fastapi-example-oms:dev .

run:
	$(MAKE) build
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
