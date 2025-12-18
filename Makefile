# Socratic Sofa - Makefile
# Common development commands for the Socratic dialogue system

.PHONY: help install dev web clean test lint format deploy precommit precommit-install precommit-update

help:  ## Show this help message
	@echo "Socratic Sofa - Development Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install project dependencies
	@echo "📦 Installing dependencies with uv..."
	uv sync
	@echo "✅ Installation complete!"

dev:  ## Run Socratic dialogue in CLI mode
	@echo "🏛️ Running Socratic dialogue (CLI)..."
	uv run socratic_sofa

web:  ## Launch Gradio web interface
	@echo "🌐 Launching Gradio web interface..."
	@echo "📍 Open http://localhost:7860 in your browser"
	uv run socratic_web

clean:  ## Clean generated files and caches
	@echo "🧹 Cleaning generated files..."
	rm -rf outputs/*.md
	rm -rf .venv
	rm -rf __pycache__
	rm -rf src/socratic_sofa/__pycache__
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Clean complete!"

test:  ## Run tests
	@echo "🧪 Running tests..."
	uv run pytest tests/ -v

lint:  ## Run linting checks
	@echo "🔍 Running linting..."
	uv run ruff check src/

format:  ## Format code with ruff
	@echo "✨ Formatting code..."
	uv run ruff format src/

# =============================================================================
# Pre-commit Hooks
# =============================================================================

precommit-install:  ## Install pre-commit hooks
	@echo "🔧 Installing pre-commit hooks..."
	uv pip install pre-commit
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg
	@echo "✅ Pre-commit hooks installed!"

precommit:  ## Run pre-commit on all files
	@echo "🔍 Running pre-commit checks..."
	uv run pre-commit run --all-files

precommit-update:  ## Update pre-commit hooks to latest versions
	@echo "📦 Updating pre-commit hooks..."
	uv run pre-commit autoupdate
	@echo "✅ Hooks updated!"

security:  ## Run security checks only
	@echo "🔒 Running security checks..."
	uv run bandit -c pyproject.toml -r src/
	uv run pre-commit run detect-secrets --all-files

typecheck:  ## Run type checking
	@echo "🔬 Running type checks..."
	uv run mypy src/ --ignore-missing-imports

deploy-hf:  ## Deploy to Hugging Face Spaces (requires HF_TOKEN)
	@echo "🚀 Deploying to Hugging Face Spaces..."
	@if [ -z "$$HF_TOKEN" ]; then \
		echo "❌ Error: HF_TOKEN environment variable not set"; \
		echo "Set it with: export HF_TOKEN=your_token"; \
		exit 1; \
	fi
	@echo "📦 Creating Space configuration..."
	@echo "sdk: gradio" > space.yml
	@echo "sdk_version: 6.1.0" >> space.yml
	@echo "app_file: src/socratic_sofa/gradio_app.py" >> space.yml
	@echo "✅ Ready to deploy! Push this repository to Hugging Face Spaces"

run-example:  ## Run example Socratic dialogue
	@echo "💭 Running example dialogue on 'What is justice?'..."
	uv run socratic_sofa

setup-env:  ## Create .env file template
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env template..."; \
		echo "ANTHROPIC_API_KEY=your_api_key_here" > .env; \
		echo "✅ .env file created. Please add your Anthropic API key."; \
	else \
		echo "⚠️  .env file already exists. Skipping."; \
	fi

check-api:  ## Verify API key is configured
	@echo "🔑 Checking API configuration..."
	@if [ -z "$$ANTHROPIC_API_KEY" ] && ! grep -q "ANTHROPIC_API_KEY" .env 2>/dev/null; then \
		echo "❌ ANTHROPIC_API_KEY not found"; \
		echo "Run 'make setup-env' and add your API key to .env"; \
		exit 1; \
	else \
		echo "✅ API key configured"; \
	fi

build:  ## Build the project
	@echo "🔨 Building project..."
	uv build

update:  ## Update dependencies
	@echo "📦 Updating dependencies..."
	uv lock --upgrade
	uv sync

outputs:  ## View latest dialogue outputs
	@echo "📄 Latest Dialogue Outputs"
	@echo "=========================="
	@echo ""
	@echo "📜 Topic:"
	@cat outputs/01_topic.md 2>/dev/null || echo "No output file found"
	@echo ""
	@echo "❓ First Inquiry:"
	@cat outputs/02_proposition.md 2>/dev/null || echo "No output file found"
	@echo ""
	@echo "🔄 Alternative Inquiry:"
	@cat outputs/03_opposition.md 2>/dev/null || echo "No output file found"
	@echo ""
	@echo "⚖️ Judgment:"
	@cat outputs/04_judgment.md 2>/dev/null || echo "No output file found"

.DEFAULT_GOAL := help
