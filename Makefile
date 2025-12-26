.PHONY: help setup install test lint format clean run updategit

help:
	@echo "Available commands:"
	@echo "  make setup    - Set up the project (create venv, install deps)"
	@echo "  make install  - Install dependencies"
	@echo "  make test     - Run tests with pytest"
	@echo "  make lint     - Run linters (ruff, mypy)"
	@echo "  make format   - Format code with black"
	@echo "  make clean    - Clean up temporary files"
	@echo "  make run      - Run a specific experiment (usage: make run FILE=storage_example.py)"
	@echo "  make updategit m='msg' - Add, commit, and push changes (default m='more updates')"

setup:
	@bash scripts/setup.sh

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest --cov=src tests/ -v

test-watch:
	pytest-watch

lint:
	ruff check src/ tests/
	mypy src/

format:
	black src/ tests/
	ruff check --fix src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/

run:
	@if [ -z "$(FILE)" ]; then \
		echo "Error: Please specify a file to run using FILE=filename.py"; \
		echo "Example: make run FILE=storage_example.py"; \
		exit 1; \
	fi
	python src/experiments/$(FILE)

m ?= more updates

git:
	@if [ -n "$$(git status --porcelain)" ]; then \
		git add .; \
		git commit -m "$(m)"; \
		git push origin main; \
	else \
		echo "Nothing to commit, working tree clean"; \
	fi
