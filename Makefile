.PHONY: help install dev clean test build deploy run-backend db-upgrade db-revise

help:
	@echo "Bestellsystem - Available commands:"
	@echo "  make install     - Install all dependencies (backend + frontend)"
	@echo "  make dev        - Start development servers"
	@echo "  make run-backend - Start Flask backend development server"
	@echo "  make clean      - Clean build artifacts and caches"
	@echo "  make test       - Run all tests"
	@echo "  make build      - Build for production"
	@echo "  make deploy     - Deploy to production"
	@echo "  make db-upgrade  - Run database migrations"
	@echo "  make db-revise   - Create a new database migration (use: make db-revise msg=\"description\")"

install:
	@echo "Installing backend dependencies..."
	cd backend && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

dev:
	@echo "Starting development servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@make -j2 dev-backend dev-frontend

dev-backend:
	cd backend && . venv/bin/activate && python manage.py runserver

run-backend:
	cd backend && . venv/bin/activate && flask --app bestellsystem.app:create_app run --host=0.0.0.0 --port=8000 --debug

dev-frontend:
	cd frontend && npm run dev

clean:
	@echo "Cleaning build artifacts..."
	rm -rf backend/__pycache__ backend/**/__pycache__
	rm -rf backend/venv
	rm -rf frontend/node_modules
	rm -rf frontend/dist

test:
	@echo "Running tests..."
	cd backend && . venv/bin/activate && pytest
	cd frontend && npm test

build:
	@echo "Building for production..."
	cd frontend && npm run build

deploy:
	@echo "Deploying to production..."
	@echo "See README.md for deployment instructions"

db-upgrade:
	@echo "Running database migrations..."
	cd backend && . venv/bin/activate && alembic upgrade head

db-revise:
	@echo "Creating new database migration..."
	@if [ -z "$(msg)" ]; then \
		echo "Error: msg parameter is required. Usage: make db-revise msg=\"your migration message\""; \
		exit 1; \
	fi
	cd backend && . venv/bin/activate && alembic revision --autogenerate -m "$(msg)"
