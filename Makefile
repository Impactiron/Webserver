.PHONY: help install dev clean test build deploy

help:
	@echo "Bestellsystem - Available commands:"
	@echo "  make install     - Install all dependencies (backend + frontend)"
	@echo "  make dev        - Start development servers"
	@echo "  make clean      - Clean build artifacts and caches"
	@echo "  make test       - Run all tests"
	@echo "  make build      - Build for production"
	@echo "  make deploy     - Deploy to production"

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
