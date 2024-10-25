DOCKER_COMPOSE_FILE=docker-compose.yml
APP_SERVICE_NAME=fastapi
SCRIPT_DIR=scripts
SCRIPT_FILE=start.sh
ENVIRONMENT=localhost


# Bring up services
up:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d
	@echo "Waiting for $(APP_SERVICE_NAME) to be healthy..."
	@./scripts/wait-for-it.sh $(ENVIRONMENT) 8000 -- echo "Service $(APP_SERVICE_NAME) is up!"
	@cd ..
	@$(MAKE) apply-migrations  # Run migrations-apply after the service is up

# Bring down services
down:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

# Generate migrations
generate-migrations:
	@if docker ps --filter "name=$(APP_SERVICE_NAME)" --format '{{.Names}}' | grep -wq $(APP_SERVICE_NAME); then \
		echo "Creating migrations..."; \
		read -p "Enter migration message: " message; \
		docker compose exec $(APP_SERVICE_NAME) bash -c "cd $(SCRIPT_DIR) && ./$(SCRIPT_FILE) 2 '$$message'"; \
	else \
		echo "Docker service $(APP_SERVICE_NAME) is not running."; \
		exit 1; \
	fi

# Apply migrations
apply-migrations:
	@if docker ps --filter "name=$(APP_SERVICE_NAME)" --format '{{.Names}}' | grep -wq $(APP_SERVICE_NAME); then \
		echo "Applying migrations..."; \
		docker compose exec $(APP_SERVICE_NAME) bash -c "cd $(SCRIPT_DIR) && ./$(SCRIPT_FILE) 1"; \
	else \
		echo "Docker service $(APP_SERVICE_NAME) is not running."; \
		exit 1; \
	fi

# Downgrade migrations
downgrade-migrations:
	@if docker ps --filter "name=$(APP_SERVICE_NAME)" --format '{{.Names}}' | grep -wq $(APP_SERVICE_NAME); then \
		echo "Downgrading migrations..."; \
		docker compose exec $(APP_SERVICE_NAME) bash -c "cd $(SCRIPT_DIR) && ./$(SCRIPT_FILE) 3"; \
	else \
		echo "Docker service $(APP_SERVICE_NAME) is not running."; \
		exit 1; \
	fi

# Seed initial data
seed-initial-data:
	@if docker ps --filter "name=$(APP_SERVICE_NAME)" --format '{{.Names}}' | grep -wq $(APP_SERVICE_NAME); then \
		echo "Seeding initial data..."; \
		docker compose exec $(APP_SERVICE_NAME) bash -c "cd $(SCRIPT_DIR) && ./$(SCRIPT_FILE) 4"; \
	else \
		echo "Docker service $(APP_SERVICE_NAME) is not running."; \
		exit 1; \
	fi
