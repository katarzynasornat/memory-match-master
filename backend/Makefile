.PHONY: install run dev test help

# Default target
help:
	@echo "Usage:"
	@echo "  make install    - Install dependencies using uv"
	@echo "  make run        - Run the production server (no reload)"
	@echo "  make dev        - Run the development server (with hot-reload)"
	@echo "  make test       - Run the test suite"

install:
	uv sync

run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 3000

dev:
	uv run uvicorn app.main:app --reload --port 3000

test:
	uv run pytest tests/
