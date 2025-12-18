# Hugging Face Spaces Deployment Checklist

Quick reference guide for deploying Socratic Sofa to Hugging Face Spaces.

## 📋 Pre-Deployment Checklist

- [x] `app.py` - Entry point configured
- [x] `requirements.txt` - All dependencies listed
- [x] `HF_README.md` - Space metadata and description
- [x] `.env.example` - Environment variable documentation
- [x] `src/socratic_sofa/` - Source code ready
- [x] Gradio 6.0 compatibility - CSS parameter fixed
- [ ] `.env` file with `ANTHROPIC_API_KEY` (local testing only)

## 🚀 Deployment Steps

### Method 1: Web UI (Recommended for First Time)

1. **Create Space**
   - Go to: https://huggingface.co/new-space
   - Name: `socratic-sofa` (or your choice)
   - SDK: **Gradio**
   - SDK Version: 6.1.0
   - License: MIT
   - Visibility: Public

2. **Upload Files**
   - Upload these files via web UI:
     ```
     app.py
     requirements.txt
     README.md (copy HF_README.md as README.md)
     src/socratic_sofa/ (entire directory)
     ```

3. **Set API Key**
   - Go to: Space Settings → Variables and Secrets
   - Add secret: `ANTHROPIC_API_KEY` = `your_anthropic_api_key`
   - Click "Save"

4. **Wait for Build**
   - Space will build automatically (2-3 minutes)
   - Check logs for any errors
   - Once complete, your Space is live!

### Method 2: Git Push (For Updates)

```bash
# 1. Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/socratic-sofa
cd socratic-sofa

# 2. Copy project files
cp /path/to/socratic_sofa/app.py .
cp /path/to/socratic_sofa/requirements.txt .
cp /path/to/socratic_sofa/HF_README.md README.md
cp -r /path/to/socratic_sofa/src .

# 3. Commit and push
git add .
git commit -m "Deploy to Hugging Face Spaces"
git push

# 4. Add API key via web UI (first time only)
# Go to Space Settings → Variables and Secrets
```

## 📁 File Structure for HF Spaces

```
socratic-sofa/
├── app.py                    # Entry point (required)
├── requirements.txt          # Dependencies (required)
├── README.md                 # Space metadata (required)
└── src/
    └── socratic_sofa/
        ├── __init__.py
        ├── gradio_app.py     # Main Gradio interface
        ├── crew.py           # CrewAI orchestration
        ├── content_filter.py # Content moderation
        ├── topics.yaml       # Topic library
        ├── main.py          # CLI entry point
        ├── config/
        │   ├── agents.yaml
        │   └── tasks.yaml
        └── tools/
```

## 🔍 Verification Steps

After deployment:

1. **Check Build Logs**
   - Ensure no errors during build
   - Verify all dependencies installed

2. **Test Basic Functionality**
   - Visit your Space URL
   - Try "Let AI choose" option
   - Verify dialogue generates correctly

3. **Test Topic Selection**
   - Select a topic from library
   - Enter custom topic
   - Verify both methods work

4. **Check Mobile Responsiveness**
   - Test on mobile device or browser devtools
   - Verify UI is usable on small screens

5. **Monitor Performance**
   - Check response times
   - Verify API calls are working
   - Monitor for any errors

## 🛠️ Troubleshooting

### Build Fails

**Problem**: Dependencies not installing

```
Solution: Verify requirements.txt has correct versions:
- crewai[tools]==1.7.0
- anthropic>=0.75.0
- gradio>=6.1.0
- pyyaml>=6.0.3
```

**Problem**: Module not found error

```
Solution: Check that src/ directory structure is correct
and app.py has correct path: sys.path.insert(0, str(Path(__file__).parent / "src"))
```

### Runtime Errors

**Problem**: API key not found

```
Solution:
1. Go to Space Settings → Variables and Secrets
2. Add ANTHROPIC_API_KEY
3. Restart Space
```

**Problem**: Gradio version warning

```
Solution: Already fixed! CSS parameter moved to launch() method
```

**Problem**: Content moderation blocks all topics

```
Solution: Check content_filter.py settings
Verify topics.yaml is being loaded correctly
```

### Performance Issues

**Problem**: Cold start takes long

```
Solution: This is normal for HF Spaces free tier
First request after inactivity may take 30-60 seconds
```

**Problem**: Dialogue generation is slow

```
Solution:
1. Check Anthropic API status
2. Verify API key has sufficient credits
3. Consider upgrading HF Space hardware if needed
```

## 📊 Monitoring

After deployment, monitor:

1. **Usage Metrics** (HF Spaces Dashboard)
   - Total requests
   - Active users
   - Error rate

2. **API Usage** (Anthropic Console)
   - Token consumption
   - Request count
   - Cost tracking

3. **Error Logs** (HF Spaces Logs Tab)
   - Runtime errors
   - API failures
   - Content moderation triggers

## 🔄 Updating Your Deployment

```bash
# Make changes locally
git add .
git commit -m "Update: description of changes"
git push

# Or use HF web UI to upload updated files
```

## 🎯 Next Steps

After successful deployment:

1. **Share Your Space**
   - Get shareable URL: `https://huggingface.co/spaces/YOUR_USERNAME/socratic-sofa`
   - Share on social media
   - Add to your portfolio

2. **Customize Further**
   - Add more topics to topics.yaml
   - Customize UI theme and colors
   - Add analytics tracking

3. **Monitor and Improve**
   - Gather user feedback
   - Monitor error rates
   - Optimize based on usage patterns

4. **Consider Upgrades**
   - HF Spaces Pro for better performance
   - Custom domain
   - Increased resource limits

## 📚 Additional Resources

- **Full Deployment Guide**: `docs/development/deployment.md`
- **Hugging Face Spaces Docs**: https://huggingface.co/docs/hub/spaces
- **Gradio Documentation**: https://gradio.app/docs
- **Anthropic API Docs**: https://docs.anthropic.com

## 🆘 Getting Help

If you encounter issues:

1. Check `docs/development/deployment.md` for detailed troubleshooting
2. Review HF Spaces logs for errors
3. Verify environment variables are set correctly
4. Check Anthropic API status: https://status.anthropic.com/
5. Open an issue on GitHub if problem persists

---

**Ready to deploy?** Follow the steps above and your Socratic Sofa will be live in minutes! 🎉
