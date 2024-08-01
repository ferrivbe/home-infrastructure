# Makefile for Docker Compose commands

# Variables
DOCKER_COMPOSE = docker-compose
COMPOSE_FILE = docker-compose.yml

# Targets
.PHONY: up down restart build logs

dev:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up

dev-api:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up --build api

# Start the containers
up:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up -d

# Stop the containers
down:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down

# Restart the containers
restart:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up -d

# Build or rebuild services
build:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) build

# View output from containers
logs:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) logs -f

# Remove containers, networks, volumes, and images created by up
clean:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down -v --rmi all --remove-orphans

# List all containers
ps:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) ps
