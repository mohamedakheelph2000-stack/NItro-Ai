# 🚀 Nitro AI - Laptop Server Setup Guide

## 📋 Overview

Nitro AI runs entirely on your laptop using **Ollama** (100% free local AI) with no paid APIs or cloud dependencies. You can access it from:
- ✅ Your laptop's browser (localhost)
- ✅ Mobile phones/tablets on your network
- ✅ Remote devices via Cloudflare Tunnel (optional)

---

## ⚡ Quick Start (5 Minutes)

### 1️⃣ Install Ollama
```bash
# Download from: https://ollama.com/download
# Or using terminal:
# Windows: winget install Ollama.Ollama
# Mac: brew install ollama
# Linux: curl -fsSL https://ollama.com/install.sh | sh
```

### 2️⃣ Pull an AI Model
```bash
# Recommended for laptops (choose ONE):
ollama pull llama3.2:1b   # 1.3GB - Fastest, great for chat
ollama pull phi3          # 2.3GB - Microsoft's efficient model (RECOMMENDED)
ollama pull mistral       # 4.1GB - Very capable, balanced
ollama pull llama3:8b     # 4.7GB - Highest quality
```

### 3️⃣ Start Backend Server
```powershell
cd "c:\Nitro AI\backend"
$env:PYTHONIOENCODING="utf-8"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Important:** Use `--host 0.0.0.0` to allow network access (not just 127.0.0.1)

### 4️⃣ Start Frontend
```powershell
cd "c:\Nitro AI\frontend"
python -m http.server 3000
```

### 5️⃣ Open in Browser
- **On your laptop:** http://localhost:3000
- **On mobile (same WiFi):** http://YOUR-LAPTOP-IP:3000

---

## 🔍 Find Your Laptop's IP Address

### Windows
```powershell
ipconfig | Select-String -Pattern "IPv4"
```
Example output: `192.168.1.100`

### Mac/Linux
```bash
ifconfig | grep "inet "
# Or simpler:
hostname -I
```

### Then access from mobile:
Replace `YOUR-LAPTOP-IP` with your actual IP:
```
http://192.168.1.100:3000
```

---

## 🌐 Remote Access with Cloudflare Tunnel (Optional)

Access your AI from anywhere (coffee shop, work, etc.) using Cloudflare's **free** tunnel:

### Install Cloudflare Tunnel
```bash
# Download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
```

### Start Tunnel
```powershell
cloudflared tunnel --url http://localhost:3000
```

You'll get a public URL like:
```
https://random-words-1234.trycloudflare.com
```

Share this URL to access Nitro AI from any device!

**Security Note:** The tunnel is temporary and auto-expires when you close it. For permanent access, set up a free Cloudflare account.

---

## 🎯 System Requirements

### Minimum
- **RAM:** 8GB (for llama3.2:1b)
- **Storage:** 2GB free
- **OS:** Windows 10+, macOS 11+, Ubuntu 20.04+
- **Python:** 3.11+

### Recommended
- **RAM:** 16GB (for phi3 or mistral models)
- **Storage:** 10GB free
- **GPU:** Helps but NOT required

---

## 🔧 Configuration

### Backend (.env)
Located at: `c:\Nitro AI\backend\.env`

```env
# Which AI provider (always "ollama" for local mode)
AI_MODEL=ollama

# Which model to use
OLLAMA_MODEL=phi3

# Ollama server URL (default is fine)
OLLAMA_BASE_URL=http://localhost:11434

# Server settings
HOST=0.0.0.0    # Important: allows network access
PORT=8000
```

### Frontend (config.js)
Located at: `c:\Nitro AI\frontend\config.js`

```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    // ...
};
```

**For network access**, change to your laptop's IP:
```javascript
API_BASE_URL: 'http://192.168.1.100:8000',
```

---

## 📱 Mobile Access Setup

### Step 1: Ensure Backend Uses 0.0.0.0
```powershell
# ✅ Correct (allows network access):
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# ❌ Wrong (localhost only):
python -m uvicorn main:app --port 8000
```

### Step 2: Get Your Laptop's IP
```powershell
ipconfig | Select-String -Pattern "IPv4"
# Example: 192.168.1.100
```

### Step 3: Update Frontend Config (Optional)
Edit `frontend/config.js`:
```javascript
API_BASE_URL: 'http://192.168.1.100:8000',
```

### Step 4: Allow Firewall
```powershell
# Windows Firewall - allow Python:
New-NetFirewallRule -DisplayName "Nitro AI Backend" -Direction Inbound -Program "C:\Python313\python.exe" -Action Allow
```

### Step 5: Access from Mobile
Open browser on your phone (same WiFi):
```
http://192.168.1.100:3000
```

---

## ✅ Verify Everything Works

### 1. Check Ollama
```bash
ollama --version
# Should show: ollama version 0.16.2 or higher
```

### 2. Check Ollama is Running
```bash
ollama list
# Should show your installed models (phi3, llama3.2:1b, etc.)
```

### 3. Test Ollama Directly
```bash
ollama run phi3 "Say hello"
# Should get an AI response
```

### 4. Test Backend
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
# Should return: {"status":"healthy"}
```

### 5. Test AI Endpoint
```powershell
$body = '{"message":"Hello"}' 
Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -ContentType "application/json" -Body $body -UseBasicParsing
# Should return JSON with ai_model="phi3" and ai_response with AI reply
```

---

## 🐛 Troubleshooting

### Backend says "Ollama not running"
```bash
# Check if Ollama is running:
ollama list

# If not, start it:
ollama serve

# Or on Windows, Ollama auto-starts on boot
# Check system tray for Ollama icon
```

### Can't access from mobile
1. **Firewall:** Allow Python in Windows Firewall
2. **Same Network:** Ensure phone and laptop are on same WiFi
3. **IP Address:** Double-check your laptop's IP with `ipconfig`
4. **Backend Host:** Ensure using `--host 0.0.0.0` not `127.0.0.1`

### Slow responses
- **Model too large:** Try `llama3.2:1b` instead of `llama3:8b`
- **RAM:** Close other applications
- **First run:** Model is loading, wait 10 seconds

### Frontend can't reach backend
1. **CORS:** Backend automatically allows localhost
2. **Port:** Ensure backend is on port 8000
3. **URL:** Check `config.js` has correct `API_BASE_URL`

---

## 🔐 Privacy & Security

### What Stays on Your Laptop
- ✅ All AI responses (100% local)
- ✅ Chat history (localStorage in browser)
- ✅ Your prompts and queries

### What Uses Internet
- ⚠️ Frontend static files (if using Python http.server, no internet needed)
- ⚠️ Model downloads (one-time, from Ollama)

### Complete Offline Mode
```powershell
# 1. Download models while online:
ollama pull phi3

# 2. Disconnect from internet

# 3. Start backend and frontend
cd "c:\Nitro AI\backend"
python -m uvicorn main:app --host 0.0.0.0 --port 8000

cd "c:\Nitro AI\frontend"
python -m http.server 3000

# 4. Access at http://localhost:3000
# Everything works offline!
```

---

## 🚀 Production Tips

### Auto-Start on Boot (Windows)

Create `start-nitro-ai.bat`:
```batch
@echo off
cd /d "c:\Nitro AI\backend"
set PYTHONIOENCODING=utf-8
start "Nitro AI Backend" python -m uvicorn main:app --host 0.0.0.0 --port 8000

cd /d "c:\Nitro AI\frontend"
start "Nitro AI Frontend" python -m http.server 3000
```

Place in: `C:\Users\YourName\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

### Persistent Cloudflare Tunnel

1. Create free Cloudflare account
2. Follow: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/
3. Get permanent subdomain like `nitro-ai.yourname.com`

---

## 📊 Model Comparison

| Model | Size | RAM | Speed | Quality | Best For |
|-------|------|-----|-------|---------|----------|
| llama3.2:1b | 1.3GB | 4GB | ⚡⚡⚡ | ★★☆ | Low-end laptops, speed |
| phi3 | 2.3GB | 8GB | ⚡⚡ | ★★★ | Balanced, recommended |
| mistral | 4.1GB | 12GB | ⚡ | ★★★★ | Capable responses |
| llama3:8b | 4.7GB | 16GB | ⚡ | ★★★★★ | Best quality |

---

## 🎉 You're All Set!

Your Nitro AI is now running fully locally on your laptop with:
- ✅ 100% free (no API costs)
- ✅ Private (data never leaves your device)
- ✅ Offline capable
- ✅ Network accessible (mobile, tablet)
- ✅ Optional remote access (Cloudflare Tunnel)

**Next Steps:**
1. Try chatting at http://localhost:3000
2. Set up mobile access using your laptop's IP
3. (Optional) Set up Cloudflare Tunnel for remote access

**Need help?** Check the main README or open an issue on GitHub!

---

## 📝 Quick Reference

```powershell
# Start Backend (from c:\Nitro AI\backend)
$env:PYTHONIOENCODING="utf-8"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Start Frontend (from c:\Nitro AI\frontend)
python -m http.server 3000

# Access
# Laptop: http://localhost:3000
# Mobile: http://YOUR-LAPTOP-IP:3000

# Check Ollama
ollama list                          # Show installed models
ollama ps                            # Show running models
ollama run phi3 "test prompt"        # Test a model

# Check Backend
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing

# Get Your IP
ipconfig | Select-String -Pattern "IPv4"
```

Made with ❤️ by Nitro AI Team
