# =====================================
# 🐳 Docker Commands Makefile
# =====================================

# Colors
GREEN := \033[0;32m
BLUE  := \033[1;34m
RESET := \033[0m

# Default goal
.DEFAULT_GOAL := help

# =====================================
# 🚀 Commands
# =====================================

up: ## Start containers in detached mode
        @echo "$(BLUE)Starting containers...$(RESET)"
        @docker compose up -d

down: ## Stop and remove containers
        @echo "$(BLUE)Stopping and removing containers...$(RESET)"
        @docker compose down

build: ## Build and start containers
        @echo "$(BLUE)Building and starting containers...$(RESET)"
        @docker compose up -d --build

restart: ## Restart containers
        @echo "$(BLUE)Restarting containers...$(RESET)"
        @docker compose down && docker compose up -d

rebuild: ## Remove volumes and rebuild containers
        @echo "$(BLUE)Rebuilding from scratch (with volumes)...$(RESET)"
        @docker compose down -v && docker compose up -d --build

# =====================================
# 🧭 Help Menu
# =====================================

help: ## Show this help
        @echo ""
        @echo "$(GREEN)Available commands:$(RESET)"
        @echo ""
        @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
                | sort \
                | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-12s$(RESET) %s\n", $$1, $$2}'
        @echo ""
