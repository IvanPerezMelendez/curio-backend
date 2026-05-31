.PHONY: help run_local test lint format check_all docker_up docker_down docker_logs

PYTHON := uv run
FASTAPI := fastapi
SRC := src/main.py

help:
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

run_local: ## Ejecutar servidor en desarrollo (hot-reload en :8000. Make sure to have docker compose up running)
	$(PYTHON) $(FASTAPI) dev $(SRC) --host 0.0.0.0 --port 8000

test:
	$(PYTHON) pytest tests/

docker_up:
	docker compose up -d

docker_down:
	docker compose down

docker_logs:
	docker compose logs -f

# Alembic commands (developers)
alembic_autogenerate:
	@printf "Enter migration description: "; \
	read desc; \
	uv run alembic revision --autogenerate \
	--rev-id z_$$(date +%Y%m%d%H%M%S) \
	-m "$$desc"

alembic_head:
	uv run alembic upgrade head

alembic_merge_heads:
	uv run alembic merge heads \
	--rev-id z_$$(date +%Y%m%d%H%M%S) \
	-m "merge heads" \
