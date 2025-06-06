# DubSync Makefile for easy development and deployment

.PHONY: help build up down logs clean install-backend install-frontend dev test

# Default target
help:
	@echo "DubSync - Real-Time Speech Transcription"
	@echo ""
	@echo "Available commands:"
	@echo "  build          Build all Docker containers"
	@echo "  up             Start all services with GPU support"
	@echo "  up-cpu         Start all services with CPU-only"
	@echo "  down           Stop all services"
	@echo "  logs           Show logs from all services"
	@echo "  logs-backend   Show backend logs"
	@echo "  logs-frontend  Show frontend logs"
	@echo "  clean          Remove all containers and volumes"
	@echo "  install-backend Install backend dependencies"
	@echo "  install-frontend Install frontend dependencies"
	@echo "  dev-backend    Start backend in development mode"
	@echo "  dev-frontend   Start frontend in development mode"
	@echo "  test           Run tests"
	@echo "  migrate        Run Django migrations"
	@echo "  shell          Open Django shell"
	@echo "  superuser      Create Django superuser"

# Docker commands
build:
	docker-compose build

up:
	docker-compose up -d

up-cpu:
	docker-compose -f docker-compose.cpu.yml up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# Local development
install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

dev-backend:
	cd backend && python manage.py runserver 0.0.0.0:8000

dev-frontend:
	cd frontend && npm run dev

# Django management
migrate:
	cd backend && python manage.py migrate

shell:
	cd backend && python manage.py shell

superuser:
	cd backend && python manage.py createsuperuser

# Testing
test:
	cd backend && python manage.py test
	cd frontend && npm test

# Health check
health:
	@echo "Checking backend health..."
	@curl -f http://localhost:8000/api/health/ || echo "Backend not responding"
	@echo "Checking frontend..."
	@curl -f http://localhost:3000/ || echo "Frontend not responding"

# Quick setup
setup: build up
	@echo "Waiting for services to start..."
	@sleep 30
	@make health

# Development setup
dev-setup: install-backend install-frontend
	@echo "Development environment ready!"
	@echo "Start backend: make dev-backend"
	@echo "Start frontend: make dev-frontend"