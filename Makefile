# Perception - AI News Intelligence Platform
# Makefile for development and deployment

.PHONY: help install dev test lint deploy clean

# Default target
help:
	@echo "Perception - Available Commands"
	@echo "================================"
	@echo "  make install     Install dependencies"
	@echo "  make dev         Run local development server"
	@echo "  make test        Run test suite"
	@echo "  make lint        Run linting checks"
	@echo "  make deploy      Deploy to Vertex AI Agent Engine"
	@echo "  make clean       Clean up build artifacts"
	@echo "  make docker      Build Docker image"

# Install dependencies
install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip
	. .venv/bin/activate && pip install -r requirements.txt

# Run local development server
dev:
	@chmod +x scripts/dev_run_adk.sh
	@./scripts/dev_run_adk.sh

# Run tests
test:
	. .venv/bin/activate && pytest tests/ -v --cov=app

# Run linting
lint:
	. .venv/bin/activate && flake8 app/ --max-line-length=120
	. .venv/bin/activate && mypy app/
	. .venv/bin/activate && black --check app/

# Format code
format:
	. .venv/bin/activate && black app/

# Deploy to production
deploy:
	@chmod +x scripts/deploy_agent_engine.sh
	@./scripts/deploy_agent_engine.sh

# Build Docker image
docker:
	docker build -t perception-agents:latest .

# Clean build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/ .coverage htmlcov/

# Check GCP authentication
check-auth:
	@echo "Checking GCP authentication..."
	@gcloud auth list
	@echo ""
	@echo "Current project:"
	@gcloud config get-value project

# Set up GCP project
setup-gcp:
	gcloud auth application-default login
	gcloud config set project perception-with-intent
	@echo "GCP authentication complete"
