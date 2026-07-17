# Developer convenience wrapper. See each package's README for details.
.PHONY: help backend-setup backend-check frontend-setup frontend-check infra-check dev-backend dev-frontend

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

backend-setup: ## Create venv and install backend deps
	cd backend && python3.12 -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e ".[dev]"

backend-check: ## Run backend quality gates
	cd backend && . .venv/bin/activate && ruff check . && ruff format --check . && mypy app && pytest

frontend-setup: ## Install frontend deps
	cd frontend && npm ci

frontend-check: ## Run frontend quality gates
	cd frontend && npm run lint && npm run typecheck && npm run test && npm run build

infra-check: ## Validate Terraform
	cd infra && terraform fmt -check -recursive && terraform init -backend=false && terraform validate

dev-backend: ## Run the backend locally
	cd backend && . .venv/bin/activate && uvicorn app.main:app --reload

dev-frontend: ## Run the frontend locally
	cd frontend && npm run dev
