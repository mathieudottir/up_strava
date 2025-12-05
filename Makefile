.PHONY: help build up down restart logs clean ssl-init

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

logs: ## View logs from all services
	docker-compose logs -f

logs-backend: ## View backend logs
	docker-compose logs -f backend

logs-frontend: ## View frontend logs
	docker-compose logs -f frontend

logs-nginx: ## View nginx logs
	docker-compose logs -f nginx

clean: ## Remove all containers, volumes, and images
	docker-compose down -v
	docker system prune -af

ps: ## Show running containers
	docker-compose ps

shell-backend: ## Open shell in backend container
	docker-compose exec backend /bin/sh

shell-frontend: ## Open shell in frontend container
	docker-compose exec frontend /bin/sh

shell-db: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U strava_user -d strava_gamification

backup-db: ## Backup database
	docker-compose exec postgres pg_dump -U strava_user strava_gamification > backup_$$(date +%Y%m%d_%H%M%S).sql

ssl-init: ## Initialize SSL certificates with Let's Encrypt
	@echo "Initializing SSL certificates..."
	@read -p "Enter your domain name: " domain; \
	read -p "Enter your email: " email; \
	docker-compose run --rm certbot certonly --webroot \
		--webroot-path /var/www/certbot \
		-d $$domain \
		--email $$email \
		--agree-tos \
		--no-eff-email
	docker-compose restart nginx

dev-backend: ## Run backend in development mode
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Run frontend in development mode
	cd frontend && npm run dev

install-backend: ## Install backend dependencies
	cd backend && pip install -r requirements.txt

install-frontend: ## Install frontend dependencies
	cd frontend && npm install
