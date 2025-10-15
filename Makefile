# Makefile for ChatGPT MCP News Widget

.PHONY: help install test lint format clean seed test-connection run docker-build docker-run

help:
	@echo "ChatGPT MCP News Widget - Available Commands:"
	@echo ""
	@echo "  make install          Install dependencies"
	@echo "  make test            Run tests"
	@echo "  make lint            Run linter"
	@echo "  make format          Format code"
	@echo "  make clean           Clean cache files"
	@echo "  make seed            Seed MongoDB with sample data"
	@echo "  make test-connection Test MCP connection"
	@echo "  make run             Run MCP server"
	@echo "  make docker-build    Build Docker image"
	@echo "  make docker-run      Run Docker container"
	@echo ""

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Done!"

test:
	@echo "Running tests..."
	pytest tests/ -v

lint:
	@echo "Running linter..."
	flake8 src/ tests/ --max-line-length=100
	pylint src/ tests/ --max-line-length=100

format:
	@echo "Formatting code..."
	black src/ tests/ scripts/
	isort src/ tests/ scripts/

clean:
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "Done!"

seed:
	@echo "Seeding MongoDB..."
	python scripts/seed_mongodb.py

test-connection:
	@echo "Testing MCP connection..."
	python scripts/test_mcp_connection.py

run:
	@echo "Starting MCP server..."
	python src/mcp_server.py

docker-build:
	@echo "Building Docker image..."
	docker build -t news-mcp-server .

docker-run:
	@echo "Running Docker container..."
	docker run -d -p 3000:3000 --env-file .env --name mcp-server news-mcp-server

docker-stop:
	@echo "Stopping Docker container..."
	docker stop mcp-server
	docker rm mcp-server

docker-logs:
	@echo "Showing Docker logs..."
	docker logs -f mcp-server

dev:
	@echo "Starting development environment..."
	@echo "1. Starting MongoDB (if local)..."
	@echo "2. Running MCP server..."
	python src/mcp_server.py