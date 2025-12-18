# Deployment Guide

Comprehensive guide for deploying Socratic Sofa to production environments.

## Table of Contents

- [Deployment Overview](#deployment-overview)
- [Platform Comparison](#platform-comparison)
- [Hugging Face Spaces](#hugging-face-spaces)
- [Render](#render)
- [Railway](#railway)
- [Fly.io](#flyio)
- [Docker Deployment](#docker-deployment)
- [Environment Configuration](#environment-configuration)
- [CI/CD Integration](#cicd-integration)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)

## Deployment Overview

### Deployment Requirements

**Minimum Requirements**:

- Python 3.10-3.13
- 512MB RAM (1GB+ recommended)
- 500MB disk space
- Internet connectivity for Anthropic API
- HTTPS support (required for secure API key handling)

**Application Characteristics**:

- **Type**: Web application (Gradio interface)
- **Runtime**: Python with UV package manager
- **Dependencies**: anthropic, crewai, gradio, pyyaml
- **Port**: 7860 (default, configurable)
- **Stateless**: No database required, outputs to filesystem
- **API Calls**: Requires outbound HTTPS to api.anthropic.com

### Deployment Architecture

```
┌─────────────┐
│   Internet  │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────┐
│  Platform (HF/Render)│
│  ┌───────────────┐  │
│  │ Socratic Sofa │  │
│  │  Gradio App   │  │
│  │  Port: 7860   │  │
│  └───────┬───────┘  │
│          │          │
│    Anthropic API    │
│    (External)       │
└─────────────────────┘
```

## Platform Comparison

| Feature              | Hugging Face | Render      | Railway         | Fly.io       | Docker          |
| -------------------- | ------------ | ----------- | --------------- | ------------ | --------------- |
| **Free Tier**        | Yes (2 vCPU) | Yes (512MB) | Yes ($5 credit) | Yes (3 apps) | Self-hosted     |
| **Setup Difficulty** | ⭐ Easy      | ⭐⭐ Medium | ⭐⭐ Medium     | ⭐⭐⭐ Hard  | ⭐⭐⭐⭐ Expert |
| **Build Time**       | 2-3 min      | 5-7 min     | 3-5 min         | 3-5 min      | Local           |
| **Auto-scaling**     | Limited      | Yes         | Yes             | Yes          | Manual          |
| **Custom Domain**    | Limited      | Yes (paid)  | Yes             | Yes          | Yes             |
| **Cold Starts**      | 30-60s       | 30s         | 15s             | 10s          | N/A             |
| **Best For**         | ML demos     | Web apps    | Hobby projects  | Production   | Any             |

### Recommendation by Use Case

- **Quick demo/prototype**: Hugging Face Spaces
- **Public showcase**: Hugging Face Spaces or Render
- **Personal use**: Railway or Fly.io
- **Production/enterprise**: Fly.io or Docker on cloud provider
- **Maximum control**: Docker on VPS (DigitalOcean, AWS EC2, etc.)

## Hugging Face Spaces

Hugging Face Spaces is the recommended platform for quick deployment and ML application showcases.

### Prerequisites

1. Hugging Face account (free): https://huggingface.co/join
2. Git installed locally
3. Hugging Face token: https://huggingface.co/settings/tokens

### Deployment Steps

#### Method 1: Web UI (Easiest)

1. **Create New Space**:
   - Visit https://huggingface.co/new-space
   - Space name: `socratic-sofa` (or your choice)
   - License: MIT
   - SDK: **Gradio**
   - SDK version: 6.1.0
   - Hardware: CPU Basic (free)
   - Visibility: Public or Private

2. **Upload Files**:
   - Click "Files" tab
   - Upload these files:
     ```
     app.py (your gradio_app.py renamed)
     requirements.txt
     src/socratic_sofa/ (entire directory)
     outputs/ (empty directory)
     ```

3. **Create Requirements File**:

   Create `requirements.txt`:

   ```txt
   anthropic>=0.75.0
   crewai[tools]==1.7.0
   gradio>=6.1.0
   pyyaml>=6.0.3
   ```

4. **Create App File**:

   Create `app.py` (copy from `src/socratic_sofa/gradio_app.py`):

   ```python
   #!/usr/bin/env python
   """
   Socratic Sofa - Hugging Face Spaces Entry Point
   """
   import sys
   from pathlib import Path

   # Add src to path for imports
   sys.path.insert(0, str(Path(__file__).parent / "src"))

   from socratic_sofa.gradio_app import demo

   if __name__ == "__main__":
       demo.launch()
   ```

5. **Configure Secrets**:
   - Go to Space Settings
   - Add secret: `ANTHROPIC_API_KEY` = `your_key_here`
   - Save

6. **Deploy**:
   - Space builds automatically
   - Wait 2-3 minutes
   - Access at: `https://huggingface.co/spaces/YOUR_USERNAME/socratic-sofa`

#### Method 2: Git Push (Advanced)

```bash
# 1. Create Space on HF website first, then:

# 2. Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/socratic-sofa
cd socratic-sofa

# 3. Copy project files
cp -r /path/to/socratic_sofa/src .
cp /path/to/socratic_sofa/pyproject.toml .

# 4. Create requirements.txt
cat > requirements.txt << 'EOF'
anthropic>=0.75.0
crewai[tools]==1.7.0
gradio>=6.1.0
pyyaml>=6.0.3
EOF

# 5. Create app.py (entry point)
cat > app.py << 'EOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
from socratic_sofa.gradio_app import demo

if __name__ == "__main__":
    demo.launch()
EOF

# 6. Create README.md
cat > README.md << 'EOF'
---
title: Socratic Sofa
emoji: 🏛️
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 6.1.0
app_file: app.py
pinned: false
---

# Socratic Sofa

AI-powered philosophical dialogue using the Socratic method.
EOF

# 7. Commit and push
git add .
git commit -m "Initial deployment"
git push

# 8. Add API key via web UI (Space Settings > Secrets)
```

### Custom Configuration

**Modify Space Settings** (README.md frontmatter):

```yaml
---
title: Socratic Sofa
emoji: 🏛️
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 6.1.0
app_file: app.py
pinned: true # Pin to your profile
license: mit
duplicated_from: null
python_version: 3.11 # Specify Python version
---
```

### Hugging Face CLI (Alternative)

```bash
# Install HF CLI
pip install huggingface_hub[cli]

# Login
huggingface-cli login

# Create Space
huggingface-cli repo create socratic-sofa --type space --space_sdk gradio

# Upload files
huggingface-cli upload socratic-sofa ./app.py app.py
huggingface-cli upload socratic-sofa ./requirements.txt requirements.txt
huggingface-cli upload socratic-sofa ./src src/ --repo-type space
```

## Render

Render provides a modern platform-as-a-service with excellent free tier.

### Prerequisites

1. Render account (free): https://render.com/
2. GitHub repository with your code
3. Anthropic API key

### Deployment Steps

1. **Prepare Repository**:

   Add `render.yaml` to repository root:

   ```yaml
   services:
     - type: web
       name: socratic-sofa
       env: python
       plan: free
       buildCommand: "pip install uv && uv sync"
       startCommand: "uv run socratic_web"
       envVars:
         - key: ANTHROPIC_API_KEY
           sync: false # Set manually in dashboard
         - key: PYTHON_VERSION
           value: "3.12"
   ```

2. **Create Web Service**:
   - Visit https://dashboard.render.com/
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Select branch (main)

3. **Configure Service**:
   - **Name**: socratic-sofa
   - **Environment**: Python 3
   - **Build Command**: `pip install uv && uv sync`
   - **Start Command**: `uv run socratic_web`
   - **Plan**: Free

4. **Set Environment Variables**:
   - Add `ANTHROPIC_API_KEY` = `your_key_here`
   - Add `PORT` = `7860` (if needed)

5. **Deploy**:
   - Click "Create Web Service"
   - Wait 5-7 minutes for build
   - Access at: `https://socratic-sofa.onrender.com`

### Automatic Deploys

Enable auto-deploy on push:

```yaml
# render.yaml
services:
  - type: web
    autoDeploy: true # Deploy on every push
    branch: main
```

### Custom Domain

1. Go to Service Settings
2. Click "Custom Domains"
3. Add your domain
4. Update DNS records as instructed

## Railway

Railway offers a developer-friendly platform with $5 free credit monthly.

### Prerequisites

1. Railway account: https://railway.app/
2. GitHub repository
3. Anthropic API key

### Deployment Steps

1. **Install Railway CLI** (optional):

   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Create Project**:
   - Visit https://railway.app/new
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Click "Deploy Now"

3. **Configure Build**:

   Create `railway.toml` in repository:

   ```toml
   [build]
   builder = "NIXPACKS"
   buildCommand = "pip install uv && uv sync"

   [deploy]
   startCommand = "uv run socratic_web"
   restartPolicyType = "ON_FAILURE"
   restartPolicyMaxRetries = 10
   ```

4. **Set Environment Variables**:
   - Go to project settings
   - Variables tab
   - Add `ANTHROPIC_API_KEY`
   - Add `PORT` = `7860`

5. **Generate Domain**:
   - Go to Settings → Networking
   - Click "Generate Domain"
   - Access at: `https://socratic-sofa.up.railway.app`

### Railway CLI Deployment

```bash
# Initialize project
cd socratic_sofa
railway init

# Link to Railway project
railway link

# Set environment variable
railway variables set ANTHROPIC_API_KEY=your_key_here

# Deploy
railway up
```

### Volume for Outputs (Optional)

```toml
# railway.toml
[deploy]
volumes = [
  { name = "outputs", mountPath = "/app/outputs" }
]
```

## Fly.io

Fly.io provides modern infrastructure with excellent performance and global deployment.

### Prerequisites

1. Fly.io account: https://fly.io/
2. flyctl CLI installed
3. Docker (optional but recommended)

### Deployment Steps

1. **Install flyctl**:

   ```bash
   # macOS
   brew install flyctl

   # Linux
   curl -L https://fly.io/install.sh | sh

   # Windows
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

   # Login
   flyctl auth login
   ```

2. **Create Fly App**:

   ```bash
   cd socratic_sofa
   flyctl launch

   # Answer prompts:
   # App name: socratic-sofa (or auto-generated)
   # Region: Choose closest to you
   # PostgreSQL: No
   # Redis: No
   ```

3. **Configure fly.toml**:

   Edit generated `fly.toml`:

   ```toml
   app = "socratic-sofa"
   primary_region = "sjc"

   [build]
     builder = "paketobuildpacks/builder:base"

   [env]
     PORT = "7860"
     PYTHON_VERSION = "3.12"

   [[services]]
     internal_port = 7860
     protocol = "tcp"

     [[services.ports]]
       port = 80
       handlers = ["http"]

     [[services.ports]]
       port = 443
       handlers = ["tls", "http"]

   [http_service]
     internal_port = 7860
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0
   ```

4. **Create Procfile**:

   ```bash
   echo "web: uv run socratic_web" > Procfile
   ```

5. **Set Secrets**:

   ```bash
   flyctl secrets set ANTHROPIC_API_KEY=your_key_here
   ```

6. **Deploy**:

   ```bash
   flyctl deploy

   # Check status
   flyctl status

   # View logs
   flyctl logs

   # Access app
   flyctl open
   ```

### Scaling

```bash
# Scale to specific region
flyctl scale count 1 --region sjc

# Add more regions (global deployment)
flyctl scale count 2 --region lhr,nrt

# Adjust VM size
flyctl scale vm shared-cpu-1x --memory 1024
```

### Custom Domain

```bash
# Add custom domain
flyctl certs add example.com

# Check certificate status
flyctl certs show example.com
```

## Docker Deployment

Docker provides maximum control and portability for any cloud provider.

### Dockerfile

Create `Dockerfile`:

```dockerfile
# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy project files
COPY pyproject.toml ./
COPY src/ ./src/

# Install Python dependencies
RUN uv sync --frozen

# Create outputs directory
RUN mkdir -p outputs

# Expose Gradio port
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the application
CMD ["uv", "run", "socratic_web"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: "3.8"

services:
  socratic-sofa:
    build: .
    ports:
      - "7860:7860"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./outputs:/app/outputs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Build and Run

```bash
# Build image
docker build -t socratic-sofa:latest .

# Run container
docker run -d \
  --name socratic-sofa \
  -p 7860:7860 \
  -e ANTHROPIC_API_KEY=your_key_here \
  -v $(pwd)/outputs:/app/outputs \
  socratic-sofa:latest

# Or use docker-compose
docker-compose up -d

# View logs
docker logs -f socratic-sofa

# Stop container
docker stop socratic-sofa

# Remove container
docker rm socratic-sofa
```

### Multi-Stage Build (Optimized)

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.cargo/bin:${PATH}"

COPY pyproject.toml ./
RUN uv sync --frozen --no-dev

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /app/.venv /app/.venv
COPY src/ ./src/
RUN mkdir -p outputs

ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

EXPOSE 7860

CMD ["python", "-m", "socratic_sofa.gradio_app"]
```

### Deploy to Cloud Providers

#### AWS ECS

```bash
# Build and push to ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-west-2.amazonaws.com

docker build -t socratic-sofa .
docker tag socratic-sofa:latest <account>.dkr.ecr.us-west-2.amazonaws.com/socratic-sofa:latest
docker push <account>.dkr.ecr.us-west-2.amazonaws.com/socratic-sofa:latest

# Create ECS task definition and service (via AWS Console or CLI)
```

#### Google Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/socratic-sofa
gcloud run deploy socratic-sofa \
  --image gcr.io/PROJECT_ID/socratic-sofa \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your_key
```

#### Azure Container Instances

```bash
# Create resource group
az group create --name socratic-sofa-rg --location eastus

# Deploy container
az container create \
  --resource-group socratic-sofa-rg \
  --name socratic-sofa \
  --image your-registry/socratic-sofa:latest \
  --dns-name-label socratic-sofa \
  --ports 7860 \
  --environment-variables ANTHROPIC_API_KEY=your_key
```

## Environment Configuration

### Required Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# Optional
PORT=7860                    # Server port
PYTHON_VERSION=3.12          # Python version
GRADIO_SERVER_NAME=0.0.0.0   # Bind address
DEBUG=false                  # Debug mode
```

### Platform-Specific Configuration

#### Hugging Face Spaces

```python
# Detect HF Spaces environment
import os

if "SPACE_ID" in os.environ:
    # Running on HF Spaces
    SERVER_NAME = "0.0.0.0"
    SERVER_PORT = 7860
    SHARE = False
```

#### Render

```python
# Use Render's PORT environment variable
import os

PORT = int(os.environ.get("PORT", 7860))
```

#### Railway

```python
# Railway provides PORT automatically
import os

PORT = int(os.environ.get("PORT", 7860))
```

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy-hf:
    name: Deploy to Hugging Face
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Push to HF Spaces
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          git clone https://huggingface.co/spaces/USER/socratic-sofa hf-space
          cp -r src hf-space/
          cp app.py requirements.txt hf-space/
          cd hf-space
          git add .
          git commit -m "Auto-deploy from GitHub"
          git push

  deploy-render:
    name: Deploy to Render
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Trigger Render Deploy
        env:
          RENDER_DEPLOY_HOOK: ${{ secrets.RENDER_DEPLOY_HOOK }}
        run: |
          curl -X POST $RENDER_DEPLOY_HOOK
```

## Monitoring and Maintenance

### Health Checks

```python
# Add health check endpoint to gradio_app.py
@app.route("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Log important events
logger.info("Dialogue started for topic: %s", topic)
logger.error("API call failed: %s", error)
```

### Error Tracking

Consider integrating Sentry:

```bash
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    traces_sample_rate=0.1
)
```

## Security Considerations

### API Key Security

1. **Never commit API keys** to version control
2. **Use environment variables** on all platforms
3. **Rotate keys** periodically
4. **Set usage limits** in Anthropic Console
5. **Monitor usage** for anomalies

### HTTPS/TLS

- All platforms provide HTTPS by default
- Enforce HTTPS in production
- Use secure headers

### Rate Limiting

```python
# Add rate limiting to Gradio interface
from gradio.blocks import Blocks

demo = gr.Blocks()
demo.queue(concurrency_count=3, max_size=20)  # Limit concurrent requests
```

### Input Validation

```python
def validate_topic(topic: str) -> str:
    # Limit length
    if len(topic) > 500:
        raise ValueError("Topic too long")

    # Sanitize input
    topic = topic.strip()

    # Content moderation
    is_appropriate, reason = is_topic_appropriate(topic)
    if not is_appropriate:
        raise ValueError(reason)

    return topic
```

## Troubleshooting

### Common Deployment Issues

#### Build Failures

```bash
# Problem: UV installation fails
# Solution: Use pip fallback
buildCommand = "pip install -r requirements.txt"

# Problem: Python version mismatch
# Solution: Specify version explicitly
ENV PYTHON_VERSION=3.12
```

#### Runtime Errors

```bash
# Problem: Module not found
# Solution: Check PYTHONPATH
export PYTHONPATH=/app/src:$PYTHONPATH

# Problem: Port binding error
# Solution: Use platform's PORT variable
PORT=${PORT:-7860}
```

#### API Issues

```bash
# Problem: API key not found
# Solution: Verify environment variable is set correctly

# Problem: API rate limiting
# Solution: Implement exponential backoff and reduce concurrent requests
```

### Platform-Specific Issues

#### Hugging Face Spaces

- **Cold starts**: Spaces sleep after inactivity, first request slow
- **Resource limits**: Free tier has 2 vCPU, 16GB RAM limits
- **Build timeout**: 30-minute build timeout, optimize if needed

#### Render

- **Free tier spins down**: 15-minute inactivity causes sleep
- **Build time**: Free tier builds can be slow
- **Logs retention**: Limited on free tier

#### Railway

- **Credit limits**: $5/month free credit, monitor usage
- **Build cache**: Clear build cache if issues persist
- **Networking**: Ensure correct PORT binding

## Next Steps

After deployment:

1. **Test thoroughly**: Verify all functionality works in production
2. **Monitor performance**: Track response times and errors
3. **Set up alerts**: Configure monitoring for downtime
4. **Document deployment**: Keep deployment notes for team
5. **Plan scaling**: Prepare for increased traffic if needed

## Resources

- **Hugging Face Spaces**: https://huggingface.co/docs/hub/spaces
- **Render Documentation**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app/
- **Fly.io Docs**: https://fly.io/docs/
- **Docker Documentation**: https://docs.docker.com/
- **Anthropic API Status**: https://status.anthropic.com/

---

**Need help?** Open an issue on GitHub or consult platform-specific support channels.
