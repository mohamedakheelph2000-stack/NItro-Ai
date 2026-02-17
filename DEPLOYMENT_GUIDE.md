# 🐳 Nitro AI - Deployment Guide

## Complete guide for deploying Nitro AI to various platforms

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Docker Deployment](#docker-deployment)
3. [Render (Free Hosting)](#render-deployment)
4. [HuggingFace Spaces](#huggingface-spaces)
5. [Replit](#replit-deployment)
6. [Railway](#railway-deployment)
7. [Fly.io](#flyio-deployment)
8. [VPS (DigitalOcean/AWS)](#vps-deployment)
9. [Environment Variables](#environment-variables)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

- ✅ Nitro AI code on GitHub/GitLab
- ✅ `.env` file configured
- ✅ Dependencies listed in `requirements.txt`
- ✅ Dockerfile (included)
- ✅ Account on your chosen platform

---

## 🐳 Docker Deployment

### Local Docker Testing

```bash
# Build image
docker build -t nitro-ai:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  --name nitro-ai \
  -v $(pwd)/memory:/app/memory \
  -v $(pwd)/gallery:/app/gallery \
  nitro-ai:latest

# Check logs
docker logs nitro-ai

# Stop container
docker stop nitro-ai
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  nitro-ai:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./memory:/app/memory
      - ./gallery:/app/gallery
      - ./audio:/app/audio
    environment:
      - AI_MODEL=ollama
      - OLLAMA_BASE_URL=http://localhost:11434
      - DEBUG_MODE=false
    restart: unless-stopped
    
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    restart: unless-stopped

volumes:
  ollama-data:
```

Run with:
```bash
docker-compose up -d
```

---

## 🚀 Render Deployment (FREE)

Render offers free hosting with auto-deploy from Git.

### Step 1: Prepare Repository

```bash
# Add Render configuration
cat > render.yaml << 'EOF'
services:
  - type: web
    name: nitro-ai
    env: python
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: AI_MODEL
        value: ollama
      - key: DEBUG_MODE
        value: false
EOF
```

### Step 2: Deploy

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Connect to Render:**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository
   - Render auto-detects Python

3. **Configure:**
   - **Name:** nitro-ai
   - **Environment:** Python 3
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free

4. **Add Environment Variables:**
   - Click "Environment"
   - Add variables from `.env`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Access at: `https://nitro-ai-xxxx.onrender.com`

### Limitations (Free Tier):
- Spins down after 15 min inactivity
- 750 hours/month
- Limited RAM (512MB)
- No persistent storage

---

## 🤗 HuggingFace Spaces

Best for AI/ML projects, FREE GPU available!

### Step 1: Create Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Select "Docker" as SDK
4. Name your space: `nitro-ai`

### Step 2: Prepare Files

Create `Dockerfile` (already included)

Create `README.md` for Space:
```markdown
---
title: Nitro AI
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
---

# Nitro AI - Complete AI Platform

Local AI chat, image generation, voice assistant, and web search!

## Features
- 💬 AI Chat (Ollama)
- 🎨 Image Generation (Stable Diffusion)
- 🎤 Voice Assistant
- 🔍 Web Search

Try it now! ↗️
```

### Step 3: Deploy

```bash
# Install HF CLI
pip install huggingface-hub[cli]

# Login
huggingface-cli login

# Upload
huggingface-cli upload-space \
  --repo-id YOUR_USERNAME/nitro-ai \
  --path ./ \
  --include "backend/*" "models/*" "frontend/*" "Dockerfile"
```

### Limitations:
- 16GB storage
- Auto-sleep after 48h inactivity
- Free GPU has queue

---

## 📱 Replit Deployment

Easy one-click deploy!

### Step 1: Import

1. Go to https://replit.com
2. Click "Create Repl"
3. Select "Import from GitHub"
4. Paste your repo URL

### Step 2: Configure

Create `.replit` file:
```toml
run = "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"

[nix]
channel = "stable-22_11"

[deployment]
run = ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
deploymentTarget = "cloudrun"
```

### Step 3: Deploy

1. Click "Run" to test
2. Click "Deploy" → "Deploy to Production"
3. Access at: `https://nitro-ai-username.repl.co`

### Limitations:
- Auto-stop after inactivity
- Limited CPU
- Shared resources

---

## 🚂 Railway Deployment

Modern platform with good free tier.

### Step 1: Setup

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"

### Step 2: Configure

Railway auto-detects Python. Add environment variables:

```env
AI_MODEL=ollama
DEBUG_MODE=false
PORT=8000
```

### Step 3: Deploy

1. Railway auto-deploys on push
2. Click "Generate Domain"
3. Access at: `https://nitro-ai-production.up.railway.app`

### Pricing:
- $5 free credit/month
- Pay-as-you-go after

---

## ✈️ Fly.io Deployment

Great for low-latency global deployment.

### Step 1: Install CLI

```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### Step 2: Login & Initialize

```bash
# Login
flyctl auth login

# Initialize app
flyctl launch

# Answer prompts:
# App name: nitro-ai
# Region: Choose closest
# Postgres: No
# Redis: No
```

### Step 3: Deploy

```bash
# Deploy
flyctl deploy

# Open app
flyctl open
```

### Fly.toml Configuration:

```toml
app = "nitro-ai"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  memory = '1gb'
  cpu_kind = 'shared'
  cpus = 1
```

---

## 💻 VPS Deployment (DigitalOcean/AWS)

For full control and better performance.

### Option 1: DigitalOcean Droplet

#### Create Droplet:
1. Go to DigitalOcean
2. Create Droplet
3. Ubuntu 22.04 LTS
4. $6/month (1GB RAM)

#### Setup:
```bash
# SSH into droplet
ssh root@your-droplet-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone repository
git clone https://github.com/yourusername/nitro-ai.git
cd nitro-ai

# Run with Docker
docker-compose up -d

# Setup Nginx reverse proxy
apt install nginx -y
```

#### Nginx Configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

#### Enable HTTPS:
```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Get SSL certificate
certbot --nginx -d your-domain.com

# Auto-renewal
certbot renew --dry-run
```

### Option 2: AWS EC2

Similar to DigitalOcean:
1. Launch EC2 instance (t2.micro for free tier)
2. Configure security group (ports 80, 443, 8000)
3. Follow same Docker setup

---

## 🔐 Environment Variables

### Required Variables:

```env
# AI Configuration
AI_MODEL=ollama
OLLAMA_MODEL=phi3
OLLAMA_BASE_URL=http://localhost:11434
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=500

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG_MODE=false

# Security (PRODUCTION)
ALLOWED_ORIGINS=["https://your-domain.com"]
SECRET_KEY=your-secret-key-here

# Optional Features
IMAGE_MODEL=placeholder
VOICE_STT_ENGINE=google
VOICE_TTS_ENGINE=gtts
WEB_SEARCH_MAX_RESULTS=5
```

### Generate Secret Key:
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## 🐛 Troubleshooting

### Port Already in Use:
```bash
# Find process using port 8000
lsof -i :8000
# Or on Windows
netstat -ano | findstr :8000

# Kill process
kill -9 <PID>
```

### Out of Memory:
```env
# Reduce memory usage
AI_MAX_TOKENS=200
IMAGE_MODEL=placeholder
```

### Docker Build Fails:
```bash
# Clear Docker cache
docker system prune -a

# Rebuild
docker build --no-cache -t nitro-ai .
```

### Ollama Not Connecting:
```bash
# For cloud deployment, use placeholder mode
AI_MODEL=dummy

# Or use OpenAI API instead
AI_MODEL=openai
OPENAI_API_KEY=your-key
```

### Permission Denied:
```bash
# Fix file permissions
chmod -R 755 .
chmod -R 777 memory/ gallery/ audio/
```

---

## 📊 Monitoring

### Health Check Endpoint:
```bash
curl https://your-app.com/health
```

### View Logs:

**Docker:**
```bash
docker logs -f nitro-ai
```

**Render:**
- Dashboard → Logs tab

**Railway:**
- Click on deployment → View logs

**Fly.io:**
```bash
flyctl logs
```

---

## 🔄 Updates

### Update Deployed App:

**Docker:**
```bash
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

**Render/Railway:**
- Pushes to GitHub auto-deploy

**Fly.io:**
```bash
git pull
flyctl deploy
```

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid | Best For |
|----------|-----------|------|----------|
| **Render** | ✅ 750h/month | $7/month | Small projects |
| **HuggingFace** | ✅ Always free | - | AI/ML demos |
| **Replit** | ✅ Limited | $7/month | Learning |
| **Railway** | ✅ $5 credit | Pay-as-you-go | Growing apps |
| **Fly.io** | ✅ $0 (with limits) | $2+/month | Production |
| **VPS** | ❌ | $5-10/month | Full control |

---

## ✅ Production Checklist

Before deploying to production:

- [ ] Set `DEBUG_MODE=false`
- [ ] Configure `ALLOWED_ORIGINS`
- [ ] Set strong `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Setup monitoring
- [ ] Configure backups (memory folder)
- [ ] Add rate limiting
- [ ] Test all features
- [ ] Setup error logging
- [ ] Configure CDN (optional)

---

## 🎉 Success!

Your Nitro AI is now deployed and accessible worldwide!

**Next steps:**
1. Share your deployment URL
2. Monitor performance
3. Collect user feedback
4. Add custom features
5. Scale as needed

---

**Happy deploying! 🚀**
