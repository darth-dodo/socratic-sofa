# Syncing GitHub Repository with Hugging Face Spaces

Complete guide for keeping your Socratic Sofa GitHub repository synchronized with Hugging Face Spaces deployment.

## Table of Contents

- [Overview](#overview)
- [Method 1: Automatic Sync (Recommended)](#method-1-automatic-sync-recommended)
- [Method 2: Manual Git Push](#method-2-manual-git-push)
- [Method 3: GitHub Actions (Advanced)](#method-3-github-actions-advanced)
- [Preparing Your Repository](#preparing-your-repository)
- [Troubleshooting](#troubleshooting)

## Overview

Hugging Face Spaces supports three ways to sync with GitHub:

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Automatic Sync** | No manual work, instant updates | Requires GitHub connection | Production deployments |
| **Manual Push** | Full control, simple | Requires manual action | Testing, one-off deploys |
| **GitHub Actions** | Customizable, automated | Requires setup | CI/CD pipelines |

## Method 1: Automatic Sync (Recommended)

This method automatically syncs your GitHub repo to Hugging Face every time you push.

### Step 1: Create Hugging Face Space

1. **Visit Hugging Face**: https://huggingface.co/new-space

2. **Configure Space**:
   ```
   Space name: socratic-sofa
   License: MIT
   SDK: Gradio
   SDK version: 6.1.0+
   Hardware: CPU basic (free tier)
   ```

3. **Click "Create Space"**

### Step 2: Link GitHub Repository

1. **In your new Space**, go to **Settings** (⚙️ icon)

2. **Navigate to "Repository"** section

3. **Click "Link to a GitHub repository"**

4. **Authorize Hugging Face**:
   - Click "Authorize Hugging Face"
   - Sign in to GitHub if needed
   - Grant access to your repositories

5. **Select Repository**:
   ```
   Repository: darth-dodo/socratic-sofa
   Branch: main
   Path: / (root)
   ```

6. **Enable Auto-Sync**:
   - ✅ Check "Sync on push"
   - This creates a webhook on your GitHub repo
   - Every push to `main` will trigger HF rebuild

### Step 3: Prepare Repository Structure

Hugging Face expects an `app.py` file in the repository root. Create it:

```bash
cd socratic-sofa
```

Create `app.py` in the root:

```python
#!/usr/bin/env python3
"""
Hugging Face Space Entry Point for Socratic Sofa
"""
import sys
from pathlib import Path

# Add socratic_sofa to Python path
sys.path.insert(0, str(Path(__file__).parent / "socratic_sofa" / "src"))

# Import and launch the Gradio app
from socratic_sofa.gradio_app import demo

if __name__ == "__main__":
    # Launch on Hugging Face (public, share enabled)
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
```

### Step 4: Create `requirements.txt`

Hugging Face needs a requirements file in the root:

```bash
# Extract from pyproject.toml
cat > requirements.txt << 'EOF'
crewai==1.7.0
anthropic>=0.75.0
gradio>=6.1.0
python-dotenv>=1.1.0
pyyaml>=6.0.3
EOF
```

### Step 5: Configure Environment Variables

1. **In Hugging Face Space Settings**:
   - Go to **"Variables and secrets"**
   - Click **"New secret"**

2. **Add your Anthropic API key**:
   ```
   Name: ANTHROPIC_API_KEY
   Value: sk-ant-api03-xxxxxxxxxxxxx
   Type: Secret (not visible in UI)
   ```

3. **Optionally add**:
   ```
   ANTHROPIC_MODEL=claude-sonnet-4-5-20250514
   ```

### Step 6: Create README for Hugging Face

Create `HF_README.md` that Hugging Face will display:

```markdown
---
title: Socratic Sofa
emoji: 🏛️
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 6.1.0
app_file: app.py
pinned: false
license: mit
---

# 🏛️ Socratic Sofa

AI-powered philosophical dialogue using the authentic Socratic method.

## Features

- 🤔 Socratic Philosopher Agent
- ⚖️ Dialectic Moderator for evaluation
- 📚 100 curated philosophical topics
- 🌐 Mobile-responsive web interface

## Usage

1. Select a topic from the library or enter your own
2. Click "Begin Socratic Dialogue"
3. Watch as the AI explores the topic through systematic questioning

## About

Built with CrewAI and Claude, this system follows the classical Socratic method:
- Questions, not assertions
- Exposes contradictions through elenchus
- Maintains intellectual humility
- Progressive inquiry: definition → assumption → contradiction → insight

[GitHub Repository](https://github.com/darth-dodo/socratic-sofa)
```

### Step 7: Commit and Push

```bash
# Add new files
git add app.py requirements.txt HF_README.md

# Commit
git commit -m "Add Hugging Face deployment files

- Add app.py entry point for HF Spaces
- Add requirements.txt for dependencies
- Add HF_README.md for Space description"

# Push to GitHub (triggers automatic HF sync)
git push origin main
```

### Step 8: Monitor Deployment

1. **Check Hugging Face Logs**:
   - Go to your Space
   - Click "Logs" tab
   - Watch the build process

2. **Wait for build** (2-3 minutes):
   ```
   Installing dependencies...
   Building Gradio app...
   Running on public URL...
   ```

3. **Test your Space**:
   - Visit: `https://huggingface.co/spaces/YOUR_USERNAME/socratic-sofa`
   - Try running a dialogue

### Step 9: Verify Auto-Sync

Test that auto-sync works:

```bash
# Make a small change
echo "\nAuto-sync test" >> README.md

# Commit and push
git add README.md
git commit -m "Test auto-sync"
git push origin main

# Check Hugging Face Space - should rebuild automatically
```

## Method 2: Manual Git Push

Push directly to Hugging Face Git repository.

### Step 1: Get Hugging Face Token

1. Visit: https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: "socratic-sofa-deploy"
4. Role: "write"
5. Copy the token

### Step 2: Configure Repository Structure

Follow steps 3-6 from Method 1 to create:
- `app.py`
- `requirements.txt`
- `HF_README.md`

### Step 3: Add Hugging Face Remote

```bash
# Add HF as a git remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/socratic-sofa

# Verify remotes
git remote -v
# Should show:
# origin    https://github.com/darth-dodo/socratic-sofa.git
# hf        https://huggingface.co/spaces/YOUR_USERNAME/socratic-sofa
```

### Step 4: Push to Both Remotes

```bash
# Push to GitHub
git push origin main

# Push to Hugging Face
git push hf main

# Or push both at once
git push origin main && git push hf main
```

### Step 5: Push with Authentication

If prompted for credentials:

```bash
# Use token as password
Username: YOUR_HF_USERNAME
Password: hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Or configure credential helper
git config --global credential.helper store

# Or use SSH (if configured)
git remote set-url hf git@hf.co:spaces/YOUR_USERNAME/socratic-sofa
```

### Step 6: Create Alias for Dual Push

Add to your shell config (`~/.bashrc` or `~/.zshrc`):

```bash
# Alias for pushing to both GitHub and Hugging Face
alias push-all='git push origin main && git push hf main'
```

Then use:
```bash
git commit -m "Your changes"
push-all
```

## Method 3: GitHub Actions (Advanced)

Automate deployment to Hugging Face using GitHub Actions.

### Step 1: Add Hugging Face Token to GitHub

1. Go to your GitHub repo: Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `HF_TOKEN`
4. Value: Your Hugging Face token (from Method 2, Step 1)

### Step 2: Create Workflow File

Create `.github/workflows/deploy-to-hf.yml`:

```yaml
name: Deploy to Hugging Face

on:
  push:
    branches:
      - main
  workflow_dispatch:  # Allow manual trigger

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for proper git operations

      - name: Push to Hugging Face Space
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git config --global user.name "GitHub Actions Bot"

          # Add HF remote
          git remote add hf https://HF_USER:$HF_TOKEN@huggingface.co/spaces/${{ github.repository_owner }}/socratic-sofa || true

          # Push to HF
          git push hf main --force

      - name: Wait for Space to build
        run: |
          echo "✅ Pushed to Hugging Face"
          echo "🔗 Check your space: https://huggingface.co/spaces/${{ github.repository_owner }}/socratic-sofa"
          echo "⏳ Building... (this may take 2-3 minutes)"
```

### Step 3: Customize Workflow (Optional)

Add deployment checks:

```yaml
      - name: Check Space health
        run: |
          sleep 180  # Wait 3 minutes for build

          # Check if Space is running
          STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
            "https://huggingface.co/spaces/${{ github.repository_owner }}/socratic-sofa")

          if [ $STATUS -eq 200 ]; then
            echo "✅ Space is live!"
          else
            echo "⚠️ Space returned status: $STATUS"
            exit 1
          fi
```

### Step 4: Test Workflow

```bash
# Commit workflow
git add .github/workflows/deploy-to-hf.yml
git commit -m "Add GitHub Actions for HF deployment"
git push origin main

# Watch workflow run
# Go to: GitHub repo → Actions tab
```

### Step 5: Manual Workflow Trigger

You can also trigger deployment manually:

1. Go to: GitHub repo → Actions
2. Select "Deploy to Hugging Face"
3. Click "Run workflow"
4. Select branch and run

## Preparing Your Repository

### Essential Files for Hugging Face

Your repository root should have:

```
socratic-sofa/
├── app.py                    # HF entry point (required)
├── requirements.txt          # Dependencies (required)
├── README.md                 # GitHub README
├── HF_README.md             # Hugging Face README (optional)
├── .env.example             # API key template (optional)
└── socratic_sofa/           # Your source code
    ├── src/
    │   └── socratic_sofa/
    │       ├── gradio_app.py
    │       ├── crew.py
    │       └── ...
    └── ...
```

### Minimal `app.py` Template

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add source to path
sys.path.insert(0, str(Path(__file__).parent / "socratic_sofa" / "src"))

# Import Gradio app
from socratic_sofa.gradio_app import demo

# Launch
if __name__ == "__main__":
    demo.launch()
```

### Minimal `requirements.txt`

```txt
crewai>=1.7.0
anthropic>=0.75.0
gradio>=6.1.0
python-dotenv>=1.1.0
pyyaml>=6.0.3
```

## Troubleshooting

### Issue: Build Fails on Hugging Face

**Check logs**:
1. Go to your Space
2. Click "Logs" tab
3. Look for error messages

**Common fixes**:

```bash
# Missing dependencies
# Add to requirements.txt

# Wrong Python version
# Add to HF_README.md:
---
python_version: "3.11"
---

# Path issues
# Verify app.py has correct sys.path
```

### Issue: API Key Not Working

**Verify secret**:
1. Space Settings → Variables and secrets
2. Check `ANTHROPIC_API_KEY` is set
3. Value should start with `sk-ant-api03-`

**Test locally**:
```bash
export ANTHROPIC_API_KEY=your_key
python app.py
```

### Issue: Auto-Sync Not Triggering

**Check webhook**:
1. GitHub repo → Settings → Webhooks
2. Look for Hugging Face webhook
3. Check recent deliveries for errors

**Reconnect if needed**:
1. HF Space Settings → Repository
2. Click "Disconnect"
3. Re-link to GitHub

### Issue: Push to HF Remote Fails

**Authentication error**:
```bash
# Use token in URL
git remote set-url hf https://USER:TOKEN@huggingface.co/spaces/USER/SPACE

# Or use SSH
git remote set-url hf git@hf.co:spaces/USER/SPACE
```

**Large files error**:
```bash
# Hugging Face has file size limits
# Add to .gitignore:
*.pyc
__pycache__/
.venv/
outputs/
```

### Issue: Space Shows Old Version

**Force rebuild**:
1. Go to Space Settings
2. Click "Factory reboot"
3. Wait for rebuild (2-3 minutes)

**Or push with force**:
```bash
git push hf main --force
```

## Best Practices

### 1. Use `.gitignore`

```bash
# Add to .gitignore
.env
*.pyc
__pycache__/
.venv/
outputs/
.DS_Store
```

### 2. Separate GitHub and HF READMEs

- `README.md` - Detailed, developer-focused
- `HF_README.md` - User-focused, with Space metadata

### 3. Test Locally First

```bash
# Always test before pushing
python app.py

# Verify at http://localhost:7860
```

### 4. Use Semantic Versioning

Tag releases:
```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
git push hf v1.0.0
```

### 5. Monitor Space Usage

- Check your Hugging Face quota
- Free tier: Limited compute hours
- Upgrade if needed for production

### 6. Branch Strategy

```bash
# Develop on feature branches
git checkout -b feature/new-feature

# Push to GitHub for review
git push origin feature/new-feature

# After merge to main, auto-sync handles HF
```

## Quick Reference

### Push to Both Remotes

```bash
git push origin main && git push hf main
```

### Check Sync Status

```bash
# GitHub
git log origin/main

# Hugging Face
git log hf/main

# Compare
git log origin/main..hf/main
```

### Force Sync

```bash
# Force push to HF (use with caution)
git push hf main --force
```

### View Remotes

```bash
git remote -v
```

## Next Steps

1. **Set up automatic sync** using Method 1
2. **Test deployment** with a small change
3. **Monitor Space** in Hugging Face dashboard
4. **Share your Space** with the community

**Your Space URL**: `https://huggingface.co/spaces/YOUR_USERNAME/socratic-sofa`

---

**Need help?** Check the [Hugging Face Spaces documentation](https://huggingface.co/docs/hub/spaces) or open an issue on GitHub.
