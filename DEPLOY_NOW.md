# 🚀 Quick Deployment Guide - Nitro AI v5.0

## Choose Your Platform

### Option 1: Render (Recommended - FREE) ⭐

**Why Render?**
- ✅ FREE 750 hours/month
- ✅ Automatic HTTPS
- ✅ Auto-deploy from GitHub
- ✅ Easy setup

**Steps:**

1. **Push to GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Create Render Account**
- Go to https://render.com
- Sign up with GitHub

3. **Create New Web Service**
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Render will auto-detect `render.yaml`

4. **Set Environment Variables**
Go to Environment tab and add:
```
GEMINI_API_KEY=your_actual_key_here
```
Get it from: https://makersuite.google.com/app/apikey

5. **Deploy!**
- Click "Create Web Service"
- Wait 5-10 minutes
- Your app will be live at: `https://nitro-ai-XXXX.onrender.com`

6. **Update CORS (After first deploy)**
- Copy your Render URL
- Update environment variable:
```
ALLOWED_ORIGINS=https://nitro-ai-XXXX.onrender.com
```

---

### Option 2: HuggingFace Spaces (FREE with GPU)

**Why HuggingFace?**
- ✅ FREE tier
- ✅ GPU option available
- ✅ Great for AI apps
- ✅ Public or private

**Steps:**

1. **Create Account**
- Go to https://huggingface.co
- Sign up

2. **Create New Space**
- Click "New Space"
- Choose "Docker" SDK
- Name: `nitro-ai`

3. **Configure Space**
Create `README.md` in root:
```yaml
---
title: Nitro AI
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 8000
pinned: false
---
```

4. **Push Code**
```bash
# Clone your HF space
git clone https://huggingface.co/spaces/yourusername/nitro-ai
cd nitro-ai

# Copy files
cp -r /path/to/nitro-ai/* .

# Use Dockerfile.production
mv Dockerfile.production Dockerfile

# Commit and push
git add .
git commit -m "Deploy Nitro AI"
git push
```

5. **Set Secrets**
- Go to Space Settings → Variables
- Add: `GEMINI_API_KEY=your_key`

**Access**: https://huggingface.co/spaces/yourusername/nitro-ai

---

### Option 3: Docker (Any Platform)

**For**: Railway, Fly.io, DigitalOcean, AWS, Azure, GCP

**Build & Run:**

```bash
# Build production image
docker build -f Dockerfile.production -t nitro-ai:prod .

# Run locally to test
docker run -d \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e AI_MODEL=gemini \
  -e DEBUG_MODE=false \
  --name nitro-ai \
  nitro-ai:prod

# Test
curl http://localhost:8000/health

# Should return: {"status":"healthy","version":"5.0.0"}
```

**Deploy to Registry:**

```bash
# Tag for Docker Hub
docker tag nitro-ai:prod yourusername/nitro-ai:latest

# Push
docker push yourusername/nitro-ai:latest

# Or use platform-specific registry (GCP, AWS ECR, etc.)
```

---

## Environment Variables Reference

### Required
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Recommended for Production
```env
# Deployment
DEBUG_MODE=false
LOG_LEVEL=INFO
AI_MODEL=gemini

# CORS (update with your domain)
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# AI Settings
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=500

# Features (enable as needed)
ENABLE_WEB_SEARCH=true
ENABLE_AGENTS=true
ENABLE_IMAGE_GEN=false  # Requires HUGGINGFACE_API_KEY
ENABLE_VOICE=false      # Requires GOOGLE_CLOUD_API_KEY
```

### Optional
```env
# For image generation
HUGGINGFACE_API_KEY=your_hf_key

# For voice features
GOOGLE_CLOUD_API_KEY=your_gc_key

# For caching (if using Redis)
REDIS_URL=redis://localhost:6379
```

---

## Quick Testing After Deployment

### 1. Health Check
```bash
curl https://your-app-url.com/health
```
Expected: `{"status":"healthy","version":"5.0.0"}`

### 2. Chat Test
```bash
curl -X POST https://your-app-url.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, Nitro AI!",
    "user_id": "test123"
  }'
```

### 3. Web Interface
Open browser: `https://your-app-url.com`

You should see the Nitro AI interface with 5 tabs.

### 4. API Documentation
Visit: `https://your-app-url.com/docs`

Interactive API documentation with test interface.

---

## Troubleshooting

### Issue: "502 Bad Gateway" or app won't start

**Check logs** (platform-specific):
- **Render**: View logs in dashboard
- **HuggingFace**: Check build logs
- **Docker**: `docker logs nitro-ai`

**Common fixes**:
1. Verify `GEMINI_API_KEY` is set
2. Check `PORT` environment variable (should be set automatically)
3. Ensure `requirements.txt` has all dependencies
4. Check Dockerfile builds successfully

### Issue: CORS errors in browser

**Solution**: Update `ALLOWED_ORIGINS`
```env
ALLOWED_ORIGINS=https://your-render-url.onrender.com
```

### Issue: Slow responses

**Solutions**:
1. Reduce `AI_MAX_TOKENS` to 300-400
2. Use faster AI model (gemini-flash)
3. Enable caching (Redis)

### Issue: Out of memory

**Solutions**:
1. Disable unused features:
   ```env
   ENABLE_IMAGE_GEN=false
   ENABLE_VOICE=false
   ```
2. Upgrade hosting plan
3. Optimize model parameters

---

## Post-Deployment Checklist

- [ ] Health check returns 200 OK
- [ ] Chat endpoint works
- [ ] Web interface loads
- [ ] API docs accessible (/docs)
- [ ] CORS configured for your domain
- [ ] Environment variables set correctly
- [ ] Monitoring setup (UptimeRobot, etc.)
- [ ] Custom domain configured (optional)
- [ ] SSL certificate valid (auto on most platforms)

---

## Monitoring & Maintenance

### Setup Monitoring (FREE)

**UptimeRobot** (https://uptimerobot.com)
1. Create account
2. Add monitor for `https://your-app-url.com/health`
3. Set alert email
4. Get notified if app goes down

### Check Performance

```bash
curl https://your-app-url.com/metrics
```

Returns:
- CPU usage
- Memory usage
- Active sessions
- Uptime

### Update Deployment

**Render**: 
- Push to GitHub → Auto-deploys

**HuggingFace**:
- Push to HF repo → Auto-builds

**Docker**:
```bash
# Rebuild and redeploy
docker build -f Dockerfile.production -t nitro-ai:prod .
docker push yourusername/nitro-ai:latest
```

---

## Advanced: Custom Domain

### Render
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records (shown in dashboard)
4. SSL auto-configured

### HuggingFace
1. Spaces Settings → Domain
2. Add custom domain
3. Update DNS CNAME
4. Certificate auto-issued

---

## Cost Estimates

| Platform | Monthly Cost | Notes |
|----------|--------------|-------|
| **Render** | $0 (FREE) | 750h limit, sleeps after 15min idle |
| **HuggingFace** | $0 (FREE) | Public spaces only |
| **Railway** | $5-15 | After $5 credit |
| **Fly.io** | $0-10 | 3 free machines |
| **DigitalOcean** | $6-12 | Full control |

**Recommended**: Start with Render FREE, upgrade if needed.

---

## Need Help?

- 📖 Full Guide: See [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)
- 🏗️ Architecture: See [ARCHITECTURE.md](ARCHITECTURE.md)
- ⚡ Performance: See [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md)
- 🐛 Issues: Check platform logs and error messages

---

**You're ready to deploy! Choose a platform and follow the steps above.** 🚀

For detailed platform-specific guides, see [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md).
