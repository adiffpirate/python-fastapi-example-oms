.PHONY: help run stop test test-unit test-integration clean

help:
	@echo "Available commands:"
	@echo "  run              - Run the application (development with auto-reload, debug mode)"
	@echo "  stop             - Stop the application"
	@echo "  test             - Run all tests"
	@echo "  test-unit        - Run unit tests"
	@echo "  test-integration - Run integration tests with fresh database"
	@echo "  clean            - Clean up Docker containers and volumes"

run:
	docker compose up --build -d
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
	docker build -t python-fastapi-example-oms-app:latest .
	docker run --rm --tty python-fastapi-example-oms-app:latest python -m pytest tests/unit/ -v

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
