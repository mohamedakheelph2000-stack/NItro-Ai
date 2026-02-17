# ✅ Pre-Deployment Checklist - Nitro AI v5.0

## Before You Deploy

Complete this checklist before deploying to production:

---

## 1. API Keys & Credentials

- [ ] **Gemini API Key** obtained from https://makersuite.google.com/app/apikey
  - [ ] Tested locally and verified working
  - [ ] Saved securely (password manager)
  - [ ] NOT committed to git (.gitignore verified)

- [ ] **Optional API Keys** (if enabling features):
  - [ ] HuggingFace API key (for image generation)
  - [ ] Google Cloud API key (for voice features)

---

## 2. Code & Configuration

### Backend

- [ ] **config.py** updated:
  - [ ] `VERSION = "5.0.0"`
  - [ ] `PORT` reads from environment
  - [ ] `DEBUG_MODE` defaults to `False`
  - [ ] `ALLOWED_ORIGINS` supports dynamic configuration

- [ ] **main.py** verified:
  - [ ] Frontend static files mounted
  - [ ] All endpoints working locally
  - [ ] Error handling in place
  - [ ] Logging configured properly

- [ ] **requirements.txt** complete:
  - [ ] All dependencies listed
  - [ ] Versions pinned
  - [ ] No missing imports

### Frontend

- [ ] **index.html** tested:
  - [ ] All tabs load correctly
  - [ ] Mobile responsive
  - [ ] PWA manifest valid

- [ ] **script.js** verified:
  - [ ] API endpoints use relative URLs
  - [ ] Error handling works
  - [ ] No console errors

### Docker

- [ ] **Dockerfile.production** optimized:
  - [ ] Multi-stage build
  - [ ] Non-root user
  - [ ] Health check configured
  - [ ] PORT environment variable supported

- [ ] **Test Docker build**:
  ```bash
  docker build -f Dockerfile.production -t nitro-ai:test .
  ```
  - [ ] Build completes successfully
  - [ ] Image size reasonable (~500MB)

- [ ] **Test Docker run**:
  ```bash
  docker run -d -p 8000:8000 \
    -e GEMINI_API_KEY=your_key \
    -e AI_MODEL=gemini \
    nitro-ai:test
  ```
  - [ ] Container starts successfully
  - [ ] Health check passes: `curl http://localhost:8000/health`
  - [ ] Frontend loads: http://localhost:8000
  - [ ] Chat works

---

## 3. Environment Variables

### Create .env.production

- [ ] Copy `.env.production.example` if needed
- [ ] Set all required variables:
  ```env
  GEMINI_API_KEY=your_actual_key
  DEBUG_MODE=false
  AI_MODEL=gemini
  LOG_LEVEL=INFO
  ```

### Platform-Specific Setup

**Render:**
- [ ] `render.yaml` present in root
- [ ] All environment variables documented
- [ ] Health check path set to `/health`

**HuggingFace:**
- [ ] `README_HUGGINGFACE.md` renamed to `README.md` in space
- [ ] `app_port: 8000` in README header
- [ ] Dockerfile.production renamed to Dockerfile

**Railway/Fly.io:**
- [ ] Platform configuration files ready
- [ ] Environment variables list prepared

---

## 4. Security

- [ ] **Git Security**:
  - [ ] `.env` in `.gitignore`
  - [ ] No secrets in committed code
  - [ ] No hardcoded API keys
  - [ ] `.env.production` NOT committed (template only)

- [ ] **Production Settings**:
  - [ ] `DEBUG_MODE=false`
  - [ ] Error messages don't expose internals
  - [ ] Logging doesn't include sensitive data

- [ ] **CORS Configuration**:
  - [ ] Initial deployment: `ALLOWED_ORIGINS=*`
  - [ ] After deployment: Update with actual domain
  - [ ] Multiple domains comma-separated if needed

---

## 5. Testing Locally

### Basic Tests

- [ ] **Health Check**:
  ```bash
  curl http://localhost:8000/health
  ```
  Expected: `{"status":"healthy","version":"5.0.0"}`

- [ ] **Chat Endpoint**:
  ```bash
  curl -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Hello", "user_id": "test"}'
  ```
  Expected: AI response

- [ ] **Frontend**:
  - [ ] Open http://localhost:8000
  - [ ] All 5 tabs visible
  - [ ] Chat tab works
  - [ ] No console errors

- [ ] **API Docs**:
  - [ ] Visit http://localhost:8000/docs
  - [ ] All endpoints visible
  - [ ] Can test endpoints interactively

### Feature Tests

- [ ] **Automation Agents**:
  ```bash
  curl http://localhost:8000/agent/list
  ```
  Expected: List of 3 agents

- [ ] **Metrics**:
  ```bash
  curl http://localhost:8000/metrics
  ```
  Expected: System metrics (CPU, memory, etc.)

- [ ] **Search** (if enabled):
  ```bash
  curl -X POST http://localhost:8000/search \
    -H "Content-Type: application/json" \
    -d '{"query": "test", "user_id": "test"}'
  ```

---

## 6. Platform Selection

Choose your deployment platform:

- [ ] **Render** (Recommended for beginners)
  - Pros: FREE, easy, auto-SSL
  - Cons: Sleeps after 15min idle
  - Setup time: 15 minutes

- [ ] **HuggingFace Spaces**
  - Pros: FREE, GPU option, great for AI
  - Cons: Public only on free tier
  - Setup time: 20 minutes

- [ ] **Railway**
  - Pros: Easy, $5 credit, no sleep
  - Cons: Paid after credit
  - Setup time: 15 minutes

- [ ] **Fly.io**
  - Pros: FREE tier, global CDN
  - Cons: More complex setup
  - Setup time: 30 minutes

- [ ] **Self-hosted** (VPS)
  - Pros: Full control, best performance
  - Cons: More work, ongoing costs
  - Setup time: 1-2 hours

---

## 7. Deployment Preparation

### GitHub (for Render/Railway)

- [ ] Repository created on GitHub
- [ ] All code committed:
  ```bash
  git add .
  git commit -m "Ready for production deployment"
  git push origin main
  ```
- [ ] Repository public or accessible to platform

### Files Present

- [ ] `README.md` - Main documentation
- [ ] `render.yaml` - Render configuration
- [ ] `Dockerfile.production` - Optimized Docker
- [ ] `.dockerignore` - Build optimization
- [ ] `requirements.txt` - All dependencies
- [ ] `start.sh` - Startup script (optional)
- [ ] `.env.production` - Template for env vars

---

## 8. Post-Deployment Plan

Prepare for after deployment:

- [ ] **Monitoring Setup**:
  - Platform: UptimeRobot (https://uptimerobot.com)
  - Monitor URL: Your deployed app URL + `/health`
  - Alert email configured

- [ ] **Domain Setup** (optional):
  - Domain purchased/available
  - DNS management access
  - SSL certificate plan (auto on most platforms)

- [ ] **Update CORS**:
  - Note: After first deploy, update `ALLOWED_ORIGINS`
  - Set to actual deployed URL
  - Redeploy with new setting

- [ ] **Share & Test**:
  - Test from different devices
  - Share with beta testers
  - Gather feedback

---

## 9. Documentation Review

- [ ] Read through:
  - [ ] `DEPLOY_NOW.md` - Quick deployment guide
  - [ ] `PRODUCTION_DEPLOYMENT.md` - Detailed platform guides
  - [ ] `ARCHITECTURE.md` - Understand the system

- [ ] Bookmark for reference:
  - [ ] Platform documentation (Render/HF/etc.)
  - [ ] API key sources
  - [ ] Troubleshooting guides

---

## 10. Final Checks

### Pre-Flight

- [ ] Latest code committed to git
- [ ] All tests passing locally
- [ ] Docker build succeeds
- [ ] Environment variables documented
- [ ] API keys secured
- [ ] Deployment platform account created

### Launch Confidence

Rate your confidence (1-5) for each:

- [ ] I understand what the app does: ___/5
- [ ] I know how to deploy to my chosen platform: ___/5
- [ ] I have all required API keys: ___/5
- [ ] I can troubleshoot basic issues: ___/5
- [ ] I know how to update the app: ___/5

**Target**: All 4+/5 before deploying

---

## Quick Deployment Commands

### Test Build
```bash
docker build -f Dockerfile.production -t nitro-ai:prod .
docker run -d -p 8000:8000 -e GEMINI_API_KEY=your_key nitro-ai:prod
curl http://localhost:8000/health
```

### Git Commit
```bash
git add .
git commit -m "Production ready v5.0"
git push origin main
```

### Deploy to Render
1. Go to https://render.com
2. New Web Service
3. Connect GitHub repo
4. Wait 10 minutes
5. Done! ✅

---

## Troubleshooting Checklist

If deployment fails:

- [ ] Check build logs on platform
- [ ] Verify `GEMINI_API_KEY` is set
- [ ] Test Docker build locally
- [ ] Check `PORT` environment variable
- [ ] Review platform-specific requirements
- [ ] Check `requirements.txt` for missing deps
- [ ] Verify Python version compatibility (3.11+)

---

## Success Criteria

Your deployment is successful when:

✅ Health check returns 200 OK  
✅ Frontend loads in browser  
✅ Chat functionality works  
✅ API docs accessible at /docs  
✅ No errors in logs  
✅ Metrics endpoint returns data  
✅ CORS allows frontend access  
✅ HTTPS/SSL working (auto on most platforms)

---

## Next Steps After Deployment

1. **Test Everything**:
   - All 5 tabs in frontend
   - Chat with AI
   - Try automation agents
   - Check metrics

2. **Setup Monitoring**:
   - UptimeRobot for uptime
   - Check `/metrics` daily
   - Review logs weekly

3. **Optimize**:
   - Enable caching (Redis)
   - Add rate limiting
   - Optimize AI parameters
   - See PERFORMANCE_OPTIMIZATION.md

4. **Share**:
   - Share URL with users
   - Gather feedback
   - Iterate and improve

---

**Ready to deploy? Choose your platform from `DEPLOY_NOW.md` and go! 🚀**

All items checked? You're ready for production! 🎉
