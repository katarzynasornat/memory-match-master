.PHONY: install run dev test lint format help

# Default target
help:
	@echo "Usage:"
	@echo "  make install    - Install dependencies using uv"
	@echo "  make run        - Run the production server"
	@echo "  make dev        - Run the development server (with hot-reload)"
	@echo "  make test       - Run the test suite"
	@echo "  make lint       - Run lint checks (ruff)"
	@echo "  make format     - Run code formatter (ruff)"

install:
	uv sync

run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 3000

dev:
	uv run uvicorn app.main:app --reload --port 3000

test:
	uv run pytest tests/

lint:
	uv run ruff check .

format:
	uv run ruff format .
