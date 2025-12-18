# Development Environment Setup

Complete guide for setting up a development environment for Socratic Sofa.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Development Tools](#development-tools)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Python**: >=3.10, <3.14 (Python 3.10, 3.11, 3.12, or 3.13)
- **UV Package Manager**: Latest version recommended
- **Git**: For version control
- **Text Editor/IDE**: VS Code, PyCharm, or your preferred editor

### System Requirements

- **OS**: macOS, Linux, or Windows (with WSL2 recommended)
- **RAM**: Minimum 4GB, 8GB+ recommended for smooth development
- **Disk Space**: ~500MB for dependencies and virtual environment
- **Network**: Internet connection for API calls and package installation

### API Access

- **Anthropic API Key**: Required for Claude AI model access
  - Sign up at [Anthropic Console](https://console.anthropic.com/)
  - Create an API key from your account settings
  - Ensure you have available credits or payment method configured

## Installation

### 1. Install UV Package Manager

UV is a fast Python package installer and resolver that replaces pip and manages virtual environments.

**macOS/Linux**:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Verify installation**:

```bash
uv --version
```

### 2. Clone the Repository

```bash
cd socratic_sofa
```

### 3. Install Dependencies

UV automatically creates a virtual environment and installs all dependencies:

```bash
uv sync
```

This command:

- Creates a `.venv/` directory with an isolated Python environment
- Installs all dependencies specified in `pyproject.toml`
- Locks dependencies to ensure reproducible builds
- Takes 1-2 minutes on first run

**What gets installed**:

- `anthropic>=0.75.0` - Claude AI API client
- `crewai[tools]==1.7.0` - Multi-agent orchestration framework
- `gradio>=6.1.0` - Web interface framework
- `pyyaml>=6.0.3` - YAML configuration parser

## Environment Configuration

### Create Environment File

Create a `.env` file in the project root:

```bash
# Using make command
make setup-env

# Or manually
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

### Configure API Key

Edit `.env` and replace with your actual API key:

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Security best practices**:

- Never commit `.env` to version control (already in `.gitignore`)
- Use different API keys for development/production
- Rotate keys periodically
- Set usage limits in Anthropic Console

### Verify API Configuration

```bash
make check-api
```

Expected output:

```
🔑 Checking API configuration...
✅ API key configured
```

## Development Tools

### IDE Setup

#### VS Code Recommended Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    "tamasfe.even-better-toml"
  ]
}
```

#### VS Code Settings

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.formatting.provider": "none",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true
}
```

#### PyCharm Configuration

1. **Open Project**: File → Open → Select `socratic_sofa` directory
2. **Configure Interpreter**: Settings → Project → Python Interpreter → Add → Virtualenv Environment → Existing → `.venv/bin/python`
3. **Enable Ruff**: Settings → Tools → Ruff → Enable Ruff

### Code Quality Tools

The project uses **Ruff** for both linting and formatting (replaces Black, isort, flake8, pylint).

**Check code quality**:

```bash
make lint
```

**Format code**:

```bash
make format
```

**Manual ruff usage**:

```bash
# Lint specific files
uv run ruff check src/socratic_sofa/main.py

# Format specific files
uv run ruff format src/socratic_sofa/

# Auto-fix issues
uv run ruff check --fix src/
```

### Git Hooks (Optional)

Set up pre-commit hooks to ensure code quality:

```bash
# Install pre-commit (if not already in dependencies)
uv pip install pre-commit

# Install hooks
pre-commit install
```

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
```

## Verification

### Test Installation

Run the CLI version with default topic:

```bash
make dev
```

Expected behavior:

- Crew starts execution
- Four agents run sequentially: propose_topic → propose → oppose → judge_task
- Outputs saved to `outputs/*.md`
- Takes 2-3 minutes to complete

### Test Web Interface

Start the Gradio web interface:

```bash
make web
```

Expected output:

```
🌐 Launching Gradio web interface...
📍 Open http://localhost:7860 in your browser
Running on local URL:  http://0.0.0.0:7860
```

**Test the interface**:

1. Open http://localhost:7860 in your browser
2. Select or enter a philosophical topic
3. Click "Begin Socratic Dialogue"
4. Verify all four stages render correctly

### Verify File Structure

```bash
tree -L 3 -I '__pycache__|*.pyc|.venv'
```

Expected structure:

```
socratic_sofa/
├── outputs/
│   ├── 01_topic.md
│   ├── 02_proposition.md
│   ├── 03_opposition.md
│   └── 04_judgment.md
├── src/
│   └── socratic_sofa/
│       ├── __init__.py
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       ├── content_filter.py
│       ├── crew.py
│       ├── gradio_app.py
│       ├── main.py
│       └── topics.yaml
├── pyproject.toml
├── Makefile
├── .env
└── README.md
```

## Troubleshooting

### Common Issues

#### UV Installation Failed

**Problem**: `uv: command not found`

**Solutions**:

```bash
# Ensure UV is in PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Or reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify
uv --version
```

#### Python Version Incompatible

**Problem**: `Requires Python >=3.10, <3.14`

**Solutions**:

```bash
# Check current version
python --version

# Install compatible version using pyenv
pyenv install 3.12.0
pyenv local 3.12.0

# Re-run UV sync
uv sync
```

#### API Key Not Found

**Problem**: `ANTHROPIC_API_KEY not found`

**Solutions**:

```bash
# Verify .env exists and contains key
cat .env

# Export key directly (temporary)
export ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# Verify
make check-api
```

#### Dependencies Installation Failed

**Problem**: `Failed to download/install package`

**Solutions**:

```bash
# Clear UV cache
rm -rf ~/.cache/uv

# Clear local venv
make clean

# Reinstall
uv sync

# If still failing, use verbose mode
uv sync -v
```

#### Gradio Port Already in Use

**Problem**: `Port 7860 is already in use`

**Solutions**:

```bash
# Find process using port
lsof -i :7860

# Kill process
kill -9 <PID>

# Or use different port (modify gradio_app.py)
# Change server_port=7860 to server_port=7861
```

#### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'socratic_sofa'`

**Solutions**:

```bash
# Ensure you're in project directory
pwd

# Reinstall in editable mode
uv pip install -e .

# Verify installation
uv run python -c "import socratic_sofa; print('OK')"
```

#### CrewAI Configuration Errors

**Problem**: `YAML configuration not loading`

**Solutions**:

```bash
# Verify YAML syntax
python -c "import yaml; yaml.safe_load(open('src/socratic_sofa/config/agents.yaml'))"

# Check file permissions
ls -l src/socratic_sofa/config/

# Ensure files exist
find src/socratic_sofa/config/ -name "*.yaml"
```

### Performance Issues

#### Slow Response Times

**Causes and solutions**:

- **API Rate Limits**: Check Anthropic Console for rate limits
- **Network Latency**: Test connection to api.anthropic.com
- **Model Selection**: Ensure using `claude-sonnet-4-5` not slower models
- **System Resources**: Monitor RAM/CPU usage during execution

#### Memory Issues

**Solutions**:

```bash
# Monitor memory usage
top -p $(pgrep -f socratic_sofa)

# Reduce concurrent operations (edit crew.py)
# Add memory limits if deploying with Docker
```

### Getting Help

If you encounter issues not covered here:

1. **Check logs**: Run with verbose mode

   ```bash
   uv run socratic_sofa --verbose
   ```

2. **Review CrewAI docs**: https://docs.crewai.com
3. **Check Gradio docs**: https://gradio.app/docs
4. **Anthropic API status**: https://status.anthropic.com/
5. **Open GitHub issue**: Include error logs and environment details

## Next Steps

Once your environment is set up:

1. Read [Contributing Guidelines](contributing.md) for code standards
2. Review [Testing Guide](testing.md) to understand test structure
3. Explore [Deployment Guide](deployment.md) for production setup
4. Check project [Architecture Documentation](../architecture.md)

## Additional Resources

- **UV Documentation**: https://docs.astral.sh/uv/
- **CrewAI Framework**: https://docs.crewai.com
- **Anthropic API**: https://docs.anthropic.com/
- **Gradio Framework**: https://gradio.app/docs
- **Python Packaging**: https://packaging.python.org/

---

**Note**: This setup guide assumes a Unix-like environment. Windows users should use WSL2 or adjust commands for PowerShell/CMD as needed.
