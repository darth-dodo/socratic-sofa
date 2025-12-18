# Installation Guide

Complete installation guide for Socratic Sofa, an AI-powered philosophical dialogue system.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Verifying Installation](#verifying-installation)
- [Troubleshooting](#troubleshooting)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Next Steps](#next-steps)

## Prerequisites

Before installing Socratic Sofa, ensure you have the following:

### Required Software

1. **Python 3.10 or higher (but less than 3.14)**
   - Check your version: `python --version` or `python3 --version`
   - Download from: [python.org](https://www.python.org/downloads/)
   - Note: Python 3.14+ is not yet supported by CrewAI

2. **UV Package Manager**
   - Modern Python package manager (faster than pip)
   - Installation covered in setup steps below

3. **Anthropic API Key**
   - Required for Claude Sonnet 4.5 access
   - Get your key at: [console.anthropic.com](https://console.anthropic.com/)
   - Free tier available for testing

### System Requirements

- **Operating System**: macOS, Linux, or Windows 10/11
- **RAM**: Minimum 4GB, recommended 8GB+
- **Disk Space**: ~500MB for dependencies
- **Internet Connection**: Required for API calls and installation

## Installation Methods

### Method 1: Standard Installation (Recommended)

This is the recommended method for most users.

#### Step 1: Clone the Repository

```bash
# Navigate to your projects directory
cd ~/projects  # or wherever you keep projects

# Clone the repository
git clone https://github.com/YOUR_USERNAME/socratic-sofa.git

# Navigate into the project
cd socratic-sofa/socratic_sofa
```

#### Step 2: Install UV Package Manager

UV is a fast, modern Python package manager that manages dependencies and virtual environments.

```bash
# Install UV using pip
pip install uv

# Verify installation
uv --version
```

**Expected output**: `uv 0.x.x` (version number may vary)

#### Step 3: Install Project Dependencies

```bash
# Install all dependencies and create virtual environment
uv sync
```

This command will:

- Create a virtual environment automatically
- Install CrewAI, Anthropic SDK, Gradio, and all dependencies
- Take 1-2 minutes depending on internet speed

**Expected output**:

```
Resolved XX packages in X.XXs
Installed XX packages in X.XXs
```

#### Step 4: Configure API Key

Create a `.env` file in the project root with your Anthropic API key:

```bash
# Option 1: Use the make command (if make is installed)
make setup-env

# Then edit .env and add your key
nano .env  # or use your preferred editor
```

```bash
# Option 2: Create .env file manually
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

**Important**: Replace `your_api_key_here` with your actual API key from Anthropic.

Your `.env` file should look like:

```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Step 5: Verify Installation

```bash
# Check API key configuration
make check-api

# Or manually verify
uv run python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API key configured!' if os.getenv('ANTHROPIC_API_KEY') else 'No API key found')"
```

### Method 2: Quick Setup with Make

If you have `make` installed, use the Makefile for automated setup:

```bash
# Clone repository (same as Method 1)
git clone https://github.com/YOUR_USERNAME/socratic-sofa.git
cd socratic-sofa/socratic_sofa

# Install dependencies
make install

# Create .env template
make setup-env

# Edit .env with your API key
nano .env

# Verify setup
make check-api
```

## Verifying Installation

Run these checks to ensure everything is installed correctly:

### 1. Check Python Version

```bash
python3 --version
```

**Expected**: Python 3.10.x, 3.11.x, 3.12.x, or 3.13.x

### 2. Check UV Installation

```bash
uv --version
```

**Expected**: Version 0.x.x or higher

### 3. Check Project Dependencies

```bash
uv pip list
```

**Expected packages** (versions may vary):

- `crewai` (1.7.0)
- `anthropic` (0.75.0+)
- `gradio` (6.1.0+)
- `pyyaml` (6.0.3+)

### 4. Verify API Key

```bash
make check-api
```

**Expected**: "✅ API key configured"

### 5. Test Run (Optional)

Run a quick test to ensure the system works:

```bash
# Test the CLI interface
uv run python -c "from socratic_sofa.crew import SocraticSofa; print('Import successful!')"
```

**Expected**: "Import successful!"

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Python Version Incompatibility

**Error**: `Requires Python >=3.10, <3.14`

**Solution**:

```bash
# Check your Python version
python3 --version

# If wrong version, install Python 3.12 (recommended)
# macOS: brew install python@3.12
# Ubuntu: sudo apt install python3.12
# Windows: Download from python.org
```

#### Issue 2: UV Installation Failed

**Error**: `pip: command not found` or `uv: command not found`

**Solution**:

```bash
# Ensure pip is installed
python3 -m ensurepip --upgrade

# Try installing UV again
python3 -m pip install uv

# Add to PATH if needed (macOS/Linux)
export PATH="$HOME/.local/bin:$PATH"
```

#### Issue 3: Dependencies Installation Failed

**Error**: `Failed to resolve dependencies`

**Solution**:

```bash
# Clear UV cache
uv cache clean

# Try sync again
uv sync

# If still failing, try with verbose output
uv sync --verbose
```

#### Issue 4: API Key Not Found

**Error**: `ANTHROPIC_API_KEY not found`

**Solution**:

```bash
# Verify .env file exists
ls -la .env

# Check .env file contents (don't share your real key!)
cat .env

# Ensure no extra spaces or quotes
# Correct: ANTHROPIC_API_KEY=sk-ant-api03-xxx
# Wrong: ANTHROPIC_API_KEY = "sk-ant-api03-xxx"

# If .env is missing, create it
echo "ANTHROPIC_API_KEY=your_actual_key" > .env
```

#### Issue 5: Module Import Errors

**Error**: `ModuleNotFoundError: No module named 'socratic_sofa'`

**Solution**:

```bash
# Ensure you're in the right directory
pwd  # Should show .../socratic-sofa/socratic_sofa

# Reinstall in development mode
uv sync

# Try running with uv prefix
uv run socratic_sofa
```

#### Issue 6: Permission Denied Errors

**Error**: `Permission denied` when creating files

**Solution**:

```bash
# Create outputs directory with correct permissions
mkdir -p outputs
chmod 755 outputs

# On Windows, run as Administrator if needed
```

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Most commands show detailed error messages
2. **GitHub Issues**: Search existing issues or create a new one
3. **CrewAI Documentation**: [docs.crewai.com](https://docs.crewai.com)
4. **Anthropic Support**: For API key issues, contact Anthropic support

## Platform-Specific Instructions

### macOS

#### Prerequisites Installation

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.12
brew install python@3.12

# Verify installation
python3.12 --version
```

#### Common macOS Issues

**Issue**: Command not found errors

```bash
# Add to PATH in ~/.zshrc or ~/.bash_profile
export PATH="/opt/homebrew/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"

# Reload shell configuration
source ~/.zshrc  # or source ~/.bash_profile
```

### Linux (Ubuntu/Debian)

#### Prerequisites Installation

```bash
# Update package list
sudo apt update

# Install Python 3.12
sudo apt install python3.12 python3.12-venv python3-pip

# Verify installation
python3.12 --version
```

#### Common Linux Issues

**Issue**: SSL certificate errors

```bash
# Install CA certificates
sudo apt install ca-certificates

# Update certificates
sudo update-ca-certificates
```

### Windows

#### Prerequisites Installation

1. **Download Python**: Visit [python.org/downloads](https://www.python.org/downloads/)
2. **Run installer**: Check "Add Python to PATH" during installation
3. **Verify in PowerShell/CMD**:
   ```powershell
   python --version
   ```

#### Using Windows Terminal (Recommended)

Install Windows Terminal from Microsoft Store for better command-line experience.

#### Common Windows Issues

**Issue**: UV commands not found

```powershell
# Add Python Scripts to PATH
$env:PATH += ";$env:USERPROFILE\AppData\Local\Programs\Python\Python312\Scripts"

# Make permanent via System Environment Variables
```

**Issue**: Line ending errors

```bash
# Configure git to handle line endings
git config --global core.autocrlf true
```

### Docker Installation (Alternative)

If you prefer containerized deployment:

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/socratic-sofa.git
cd socratic-sofa/socratic_sofa

# Create .env file
echo "ANTHROPIC_API_KEY=your_key" > .env

# Build and run with Docker
docker build -t socratic-sofa .
docker run -p 7860:7860 --env-file .env socratic-sofa
```

## Next Steps

Congratulations! You've successfully installed Socratic Sofa. Here's what to do next:

1. **Quick Start**: Try the [5-minute quickstart guide](./quickstart.md)
2. **First Dialogue**: Follow the [first dialogue tutorial](./first-dialogue.md)
3. **Explore Features**: Learn about customization in the main README
4. **Deploy**: Consider deploying to Hugging Face Spaces or other platforms

## Additional Resources

- **Main README**: [../README.md](../README.md)
- **Project Structure**: [../README.md#project-structure](../README.md#project-structure)
- **CrewAI Documentation**: [docs.crewai.com](https://docs.crewai.com)
- **Gradio Documentation**: [gradio.app/docs](https://gradio.app/docs)
- **Anthropic API Docs**: [docs.anthropic.com](https://docs.anthropic.com)

---

**Need help?** Open an issue on GitHub or check the troubleshooting section above.
