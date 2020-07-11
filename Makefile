help: ## View all make targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

stop: ## Stop the container stack
	@echo "Stopping all containers..."
	docker-compose stop && docker-compose down

build: ## Build the container stack
	@echo "Building containers..."
	docker-compose build

start: ## Start the container stack
	@echo "Starting up containers..."
	make build && docker-compose up

clean: ## Clean out unused docker(-compose) files
	@echo "Removing unused docker files..."
	docker system prune -af

update: ## Update repository to latest version and rebuild container stack
	@echo "Updating repository to latest version..."
	@echo "Warning: This will (temporarily) shutdown all containers."
	@read -p "Do you want to continue? [y/N]" -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy] ]]; \
	then \
		make stop && git fetch && git pull; \
	else \
		exit; \
	fi
	@echo "Some docker files and container are no longer in use."
	@read -p "Do you want to clean up unused docker files? [y/N]" -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy] ]]; \
	then \
		make clean; \
	fi
	make build
	@read -p "Do you want to start the containers back up again? [y/N]" -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy] ]]; \
	then \
		make start; \
	fi
