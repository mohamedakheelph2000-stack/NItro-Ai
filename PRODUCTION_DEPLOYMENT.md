# 🚀 Production Deployment Guide - Nitro AI

## Overview

This guide covers deploying Nitro AI to production environments. Choose the platform that best fits your needs:

- **FREE Options**: Render, HuggingFace Spaces, Replit
- **Paid Options**: Railway, Fly.io, DigitalOcean, AWS
- **Self-Hosted**: VPS with Docker

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Platform Comparisons](#platform-comparisons)
3. [Deployment Options](#deployment-options)
   - [Render (Recommended - FREE)](#render-deployment)
   - [HuggingFace Spaces](#huggingface-deployment)
   - [Replit](#replit-deployment)
   - [Railway](#railway-deployment)
   - [Fly.io](#flyio-deployment)
   - [DigitalOcean/AWS VPS](#vps-deployment)
4. [Post-Deployment](#post-deployment)
5. [Monitoring](#monitoring)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1. Prepare Your Code

```bash
# Ensure all dependencies are listed
cd backend
pip freeze > requirements.txt

# Test locally first
python -m uvicorn main:app --reload
```

### 2. Environment Variables

Create `.env.production`:
```env
# REQUIRED
APP_NAME=Nitro AI
DEBUG_MODE=false
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# AI Configuration
AI_MODEL=ollama
OLLAMA_BASE_URL=http://localhost:11434
GEMINI_API_KEY=your_gemini_key_here

# Optional Features
ENABLE_IMAGE_GEN=false
ENABLE_VOICE=true
ENABLE_WEB_SEARCH=true
```

### 3. Test Docker Build

```bash
# Build production image
docker build -f Dockerfile.production -t nitro-ai:latest .

# Test run
docker run -p 8000:8000 nitro-ai:latest

# Visit http://localhost:8000/docs
```

---

## 📊 Platform Comparisons

| Platform | Cost | Ease | Performance | Notes |
|----------|------|------|-------------|-------|
| **Render** | FREE (750h) | ⭐⭐⭐⭐⭐ | Good | Best for beginners |
| **HuggingFace** | FREE | ⭐⭐⭐⭐ | Excellent | GPU available |
| **Replit** | FREE | ⭐⭐⭐⭐⭐ | Moderate | One-click deploy |
| **Railway** | $5 credit | ⭐⭐⭐⭐ | Good | Auto-deploy from Git |
| **Fly.io** | FREE tier | ⭐⭐⭐ | Excellent | Global CDN |
| **VPS** | $5-20/mo | ⭐⭐ | Excellent | Full control |

---

## 🎯 Deployment Options

### Render Deployment (Recommended - FREE) {#render-deployment}

**Benefits**:
- ✅ FREE 750 hours/month
- ✅ Auto-deploy from GitHub
- ✅ Built-in SSL
- ✅ Easy setup

**Steps**:

#### 1. Create Account
- Go to [render.com](https://render.com)
- Sign up with GitHub

#### 2. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/nitro-ai.git
git push -u origin main
```

#### 3. Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `nitro-ai`
   - **Environment**: `Docker`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Dockerfile Path**: `Dockerfile.production`

#### 4. Set Environment Variables
```
GEMINI_API_KEY=your_key
OLLAMA_BASE_URL=http://localhost:11434
ENABLE_IMAGE_GEN=false
ENABLE_VOICE=true
ALLOWED_ORIGINS=https://nitro-ai.onrender.com
```

#### 5. Deploy
- Click "Create Web Service"
- Wait 5-10 minutes for first deploy
- Access at: `https://nitro-ai.onrender.com`

#### 6. Setup Custom Domain (Optional)
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records
4. SSL auto-configured

**Render-specific Configuration**:

Create `render.yaml`:
```yaml
services:
  - type: web
    name: nitro-ai
    env: docker
    dockerfilePath: ./Dockerfile.production
    plan: free
    healthCheckPath: /health
    envVars:
      - key: GEMINI_API_KEY
        sync: false
      - key: ALLOWED_ORIGINS
        value: https://nitro-ai.onrender.com
```

**Limitations**:
- Sleeps after 15 min inactivity (FREE plan)
- 750 hours/month limit
- No GPU support

---

### HuggingFace Spaces Deployment {#huggingface-deployment}

**Benefits**:
- ✅ FREE with GPU option
- ✅ Integrated ML model hosting
- ✅ Great for AI apps
- ✅ Public or private

**Steps**:

#### 1. Create Account
- Go to [huggingface.co](https://huggingface.co)
- Create account

#### 2. Create New Space
1. Click "New Space"
2. Choose "Docker" SDK
3. Name: `nitro-ai`
4. License: Choose appropriate

#### 3. Configure Space

Create `spaces/README.md`:
```yaml
---
title: Nitro AI
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
---

# Nitro AI - Full-Featured AI Assistant

Your personal AI assistant with chat, images, voice, and web search!
```

#### 4. Push Code
```bash
git clone https://huggingface.co/spaces/yourusername/nitro-ai
cd nitro-ai

# Copy your files
cp -r /path/to/nitro-ai/* .

# Commit and push
git add .
git commit -m "Deploy Nitro AI"
git push
```

#### 5. Set Secrets
1. Go to Space Settings → Variables
2. Add:
   - `GEMINI_API_KEY`: Your API key
   - `OLLAMA_BASE_URL`: Custom if needed

#### 6. Enable GPU (Optional)
- Settings → Hardware → Choose GPU tier
- Upgrade to paid for permanent GPU

**Access**: `https://huggingface.co/spaces/yourusername/nitro-ai`

---

### Replit Deployment {#replit-deployment}

**Benefits**:
- ✅ One-click deploy
- ✅ Built-in IDE
- ✅ Collaborative coding
- ✅ Always-on option

**Steps**:

#### 1. Import Project
1. Go to [replit.com](https://replit.com)
2. Click "+ Create Repl"
3. Choose "Import from GitHub"
4. Enter your repo URL

#### 2. Configure Repl

Create `.replit`:
```toml
run = "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000"
language = "python3"

[env]
PYTHONUNBUFFERED = "1"

[nix]
channel = "stable-22_11"

[deployment]
run = ["sh", "-c", "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000"]
deploymentTarget = "cloudrun"
```

#### 3. Set Secrets
1. Click "Secrets" (lock icon)
2. Add environment variables:
   - `GEMINI_API_KEY`
   - `ALLOWED_ORIGINS`

#### 4. Deploy
1. Click "Deploy" button
2. Choose "Production" deployment
3. Wait for deployment
4. Get public URL

**Pricing**:
- FREE: Limited hours, sleeps when idle
- Hacker Plan ($7/mo): Always-on, faster

---

### Railway Deployment {#railway-deployment}

**Benefits**:
- ✅ $5 free credit
- ✅ GitHub auto-deploy
- ✅ Easy scaling
- ✅ Built-in databases

**Steps**:

#### 1. Create Account
- Go to [railway.app](https://railway.app)
- Sign up with GitHub

#### 2. New Project
1. Click "New Project"
2. Choose "Deploy from GitHub repo"
3. Select your Nitro AI repo

#### 3. Configure
Railway auto-detects Dockerfile, but configure:

Create `railway.toml`:
```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile.production"

[deploy]
startCommand = "python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
restartPolicyType = "ON_FAILURE"
```

#### 4. Set Variables
1. Go to Variables tab
2. Add:
   - `PORT`: Railway auto-sets
   - `GEMINI_API_KEY`
   - `ALLOWED_ORIGINS`: Use Railway domain

#### 5. Deploy
- Automatic on every push to main
- Custom domains supported

**Pricing**: Pay-as-you-go after $5 credit (~$5-15/mo typical)

---

### Fly.io Deployment {#flyio-deployment}

**Benefits**:
- ✅ Global edge deployment
- ✅ FREE tier (3 VMs)
- ✅ Fast worldwide
- ✅ Auto-scaling

**Steps**:

#### 1. Install Fly CLI
```bash
# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

#### 2. Login
```bash
fly auth login
```

#### 3. Initialize App
```bash
cd /path/to/nitro-ai
fly launch

# Answer prompts:
# - App name: nitro-ai
# - Region: Choose closest
# - Database: No
# - Deploy: No (configure first)
```

#### 4. Configure `fly.toml`
```toml
app = "nitro-ai"
primary_region = "sjc"

[build]
  dockerfile = "Dockerfile.production"

[env]
  PORT = "8000"
  ALLOWED_ORIGINS = "https://nitro-ai.fly.dev"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[http_service.checks]]
  interval = "30s"
  timeout = "10s"
  grace_period = "5s"
  method = "GET"
  path = "/health"

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512
```

#### 5. Set Secrets
```bash
fly secrets set GEMINI_API_KEY=your_key
```

#### 6. Deploy
```bash
fly deploy
```

#### 7. Access
```bash
fly open
# Opens https://nitro-ai.fly.dev
```

**Scaling**:
```bash
# Scale up
fly scale memory 1024

# Add regions
fly regions add lax
```

---

### VPS Deployment (DigitalOcean/AWS) {#vps-deployment}

**Benefits**:
- ✅ Full control
- ✅ Best performance
- ✅ Custom configurations
- ✅ SSH access

**Requirements**:
- VPS with Docker support
- Domain name (optional)
- Basic Linux knowledge

**Steps**:

#### 1. Create VPS

**DigitalOcean**:
1. Create Droplet
2. Choose Ubuntu 22.04
3. Size: $6/mo (1GB RAM) minimum
4. Add SSH key

**AWS**:
1. Launch EC2 instance
2. Ubuntu Server 22.04 LTS
3. t2.small or larger
4. Configure security group (ports 80, 443, 22)

#### 2. Connect to VPS
```bash
ssh root@your_server_ip
```

#### 3. Install Docker
```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Verify
docker --version
docker-compose --version
```

#### 4. Clone Project
```bash
git clone https://github.com/yourusername/nitro-ai.git
cd nitro-ai
```

#### 5. Configure Environment
```bash
# Create production .env
nano .env.production

# Add:
GEMINI_API_KEY=your_key
ALLOWED_ORIGINS=https://yourdomain.com
```

#### 6. Deploy with Docker Compose
```bash
# Build and start
docker-compose -f docker-compose.production.yml up -d

# Check logs
docker-compose logs -f
```

#### 7. Setup Nginx Reverse Proxy

Create `/etc/nginx/sites-available/nitro-ai`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/nitro-ai /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 8. Setup SSL with Let's Encrypt
```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Get certificate
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
certbot renew --dry-run
```

#### 9. Setup Ollama (Optional - for local AI)
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull model
ollama pull phi3

# Run as service
systemctl enable ollama
systemctl start ollama
```

---

## 🔄 Post-Deployment

### 1. Verify Deployment
```bash
# Check health
curl https://your-domain.com/health

# Test chat endpoint
curl -X POST https://your-domain.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "user_id": "test"}'
```

### 2. Setup Monitoring

**Uptime Monitoring**:
- [UptimeRobot](https://uptimerobot.com) (FREE)
- [Pingdom](https://www.pingdom.com)

**Application Monitoring**:
```bash
# Check metrics endpoint
curl https://your-domain.com/metrics
```

### 3. Configure Backups

**Render/Railway**: Automatic backups
**VPS**: Setup cron job
```bash
# Backup script
crontab -e

# Add daily backup at 2 AM
0 2 * * * docker exec nitro-ai tar czf /app/backup-$(date +\%Y\%m\%d).tar.gz /app/memory
```

---

## 📊 Monitoring

### Built-in Metrics
Access: `https://your-domain.com/metrics`

Returns:
- CPU usage
- Memory usage
- Active sessions
- Total messages
- Uptime

### External Monitoring

**1. Uptime Robot** (FREE):
- Monitor: `https://your-domain.com/health`
- Alert via email/SMS on downtime

**2. Application Logs**:
```bash
# Docker logs
docker logs nitro-ai-backend -f

# System logs
tail -f /var/log/nginx/access.log
```

---

## 🔧 Troubleshooting

### Issue: App Not Starting

**Check**:
```bash
# Container logs
docker logs nitro-ai-backend

# Container status
docker ps -a

# Restart
docker-compose restart
```

### Issue: 502 Bad Gateway

**Solutions**:
1. Check if app is running: `docker ps`
2. Check port mapping: `docker port nitro-ai-backend`
3. Check Nginx config: `nginx -t`
4. Restart services

### Issue: Slow Response Times

**Optimize**:
1. Enable Redis caching
2. Increase container resources
3. Use CDN for frontend
4. Check `/metrics` endpoint

### Issue: Out of Memory

**Solutions**:
1. Increase RAM limit in `docker-compose.yml`
2. Enable swap on VPS
3. Optimize model loading (lazy load)
4. Clear old sessions

---

## 💰 Cost Estimates

| Platform | Monthly Cost | Notes |
|----------|-------------|-------|
| Render FREE | $0 | 750h limit, sleeps |
| HuggingFace | $0 | Public only |
| Replit FREE | $0 | Limited hours |
| Railway | $5-15 | After free credit |
| Fly.io | $0-10 | 3 free VMs |
| DigitalOcean | $6-12 | Full control |

---

## ✅ Deployment Checklist

- [ ] Test locally with Docker
- [ ] Set all environment variables
- [ ] Push code to GitHub
- [ ] Choose deployment platform
- [ ] Deploy application
- [ ] Test /health endpoint
- [ ] Test /chat endpoint
- [ ] Setup custom domain (optional)
- [ ] Configure SSL
- [ ] Setup monitoring
- [ ] Configure backups
- [ ] Test all features (chat, image, voice, search)

---

## 🎯 Next Steps

After deployment:
1. Monitor performance via `/metrics`
2. Setup alerting for downtime
3. Configure CDN for frontend (Cloudflare)
4. Implement rate limiting
5. Setup CI/CD pipeline
6. Add load balancing (if needed)

---

**Your Nitro AI is now deployed and accessible worldwide! 🚀**

For support, check logs and metrics first, then consult platform-specific docs.
