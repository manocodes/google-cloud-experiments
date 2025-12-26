.PHONY: help setup install test lint format clean run gitupdate

help:
	@echo "Available commands:"
	@echo "  make setup    - Set up the project (create venv, install deps)"
	@echo "  make install  - Install dependencies"
	@echo "  make test     - Run tests with pytest"
	@echo "  make lint     - Run linters (ruff, mypy)"
	@echo "  make format   - Format code with black"
	@echo "  make clean    - Clean up temporary files"
	@echo "  make run      - Run a specific experiment (usage: make run FILE=storage_example.py)"
	@echo "  make gitupdate [msg]   - Add, commit, and push changes. Can use m='msg' or just 'msg' after command."

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

# Handle positional arguments for gitupdate
ifeq (gitupdate,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments
  MESSAGE := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(MESSAGE):;@:)
endif

gitupdate:
	@if [ -n "$$(git status --porcelain)" ]; then \
		git add .; \
		if [ -n "$(MESSAGE)" ]; then \
			git commit -m "$(MESSAGE)"; \
		else \
			git commit -m "$(m)"; \
		fi; \
		git push origin main; \
	else \
		echo "Nothing to commit, working tree clean"; \
	fi
