# 📦 Nitro AI v5.0 - Complete Setup Guide

## From zero to AI platform in 30 minutes!

---

## 📋 What You'll Build

By the end of this guide, you'll have:

- ✅ **AI Chat** - Local ChatGPT with Ollama phi3
- ✅ **Image Generation** - Create images from text (Stable Diffusion)
- ✅ **Voice Assistant** - Speech-to-text and text-to-speech
- ✅ **Web Search** - AI-powered search with citations
- ✅ **Mobile App** - Install as PWA on phone
- ✅ **Professional UI** - ChatGPT-style interface with dark mode

**Total Cost: $0/month!** 🎉

---

## 🖥️ System Requirements

### Minimum (Chat Only):
- **CPU:** 2 cores
- **RAM:** 4GB
- **Storage:** 10GB
- **OS:** Windows 10+, macOS 10.14+, Linux

### Recommended (All Features):
- **CPU:** 4+ cores (for image generation)
- **RAM:** 8GB+ (16GB for fast image gen)
- **Storage:** 20GB (for AI models)
- **GPU:** Optional (NVIDIA 4GB+ speeds up images)

---

## 🚀 Quick Start (5 Minutes)

### 1. Install Prerequisites

**Windows:**
```powershell
# Install Python 3.11
# Download from: https://www.python.org/downloads/

# Install Ollama
# Download from: https://ollama.ai/download/windows
```

**macOS:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Install Ollama
brew install ollama
```

**Linux (Ubuntu/Debian):**
```bash
# Install Python
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Install Ollama
curl https://ollama.ai/install.sh | sh
```

### 2. Clone/Download Nitro AI

```bash
# Option A: Clone with Git
git clone https://github.com/yourusername/nitro-ai.git
cd nitro-ai

# Option B: Download ZIP
# Extract to c:\Nitro AI or ~/nitro-ai
```

### 3. Setup Backend

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install core dependencies
pip install fastapi uvicorn aiohttp python-dotenv

# Start Ollama (in separate terminal)
ollama serve

# Pull AI model
ollama pull phi3

# Copy environment file
cp .env.example .env

# Start backend
python -m uvicorn main:app --reload
```

### 4. Open Frontend

```bash
# Open in browser
start frontend/index.html  # Windows
open frontend/index.html   # macOS
xdg-open frontend/index.html  # Linux

# Or use VS Code Live Server
# Right-click index.html → Open with Live Server
```

### 5. Test!

1. Open http://localhost:8000/docs
2. Try `/chat` endpoint
3. Send message: `{"message": "Hello!", "user_id": "test"}`
4. Get real AI response! 🎉

---

## 📦 Full Installation (All Features)

### Install All Dependencies:

```bash
# Navigate to project root
cd "c:\Nitro AI"  # or ~/nitro-ai

# Activate virtual environment
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install EVERYTHING
pip install -r requirements.txt

# Install optional features:

# 1. Image Generation (Stable Diffusion)
pip install diffusers torch transformers pillow
# Note: First download is ~4GB, takes time

# 2. Voice Assistant
pip install SpeechRecognition gTTS pyttsx3
# For microphone: pip install pyaudio

# 3. Web Search
pip install beautifulsoup4
# aiohttp already installed

# 4. Document Generation
# Already included in requirements.txt
```

### Special: PyAudio Installation

**Windows:**
```powershell
# Download precompiled wheel
# Go to: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Download: PyAudio‑0.2.11‑cp311‑cp311‑win_amd64.whl

# Install wheel
pip install PyAudio‑0.2.11‑cp311‑cp311‑win_amd64.whl
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

---

## ⚙️ Configuration

### 1. Edit `.env` File

```env
# ========================================
# AI MODEL CONFIGURATION
# ========================================

# Model Type: "ollama" (local, free) or "openai" (cloud, paid)
AI_MODEL=ollama

# Ollama Settings (for local AI)
OLLAMA_MODEL=phi3
OLLAMA_BASE_URL=http://localhost:11434
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=500

# OpenAI Settings (optional, for cloud AI)
# OPENAI_API_KEY=sk-your-key-here
# OPENAI_MODEL=gpt-3.5-turbo

# ========================================
# IMAGE GENERATION
# ========================================

# Image Model: "stable-diffusion" or "placeholder"
IMAGE_MODEL=placeholder  # Change to "stable-diffusion" when ready
IMAGE_DEVICE=cpu         # or "cuda" for GPU
IMAGE_LOW_MEMORY=true    # Enable for laptops

# ========================================
# VOICE ASSISTANT
# ========================================

# Speech-to-Text Engine: "google" (online, free)
VOICE_STT_ENGINE=google

# Text-to-Speech Engine: "gtts" (online) or "pyttsx3" (offline)
VOICE_TTS_ENGINE=gtts

# Default Language
VOICE_LANGUAGE=en

# ========================================
# WEB SEARCH
# ========================================

WEB_SEARCH_MAX_RESULTS=5
WEB_SEARCH_TIMEOUT=10

# ========================================
# SERVER CONFIGURATION
# ========================================

HOST=127.0.0.1
PORT=8000
DEBUG_MODE=true
LOG_LEVEL=INFO
VERSION=5.0.0

# ========================================
# FRONTEND CONFIGURATION
# ========================================

ALLOWED_ORIGINS=["http://localhost:3000", "http://127.0.0.1:5500"]

# ========================================
# FEATURE FLAGS
# ========================================

ENABLE_IMAGE_GEN=false
ENABLE_VOICE=false
ENABLE_WEB_SEARCH=true
ENABLE_VIDEO_GEN=false
ENABLE_DOCUMENT_GEN=true
```

### 2. Enable Features Gradually

**Start with chat only:**
```env
AI_MODEL=ollama
IMAGE_MODEL=placeholder
ENABLE_IMAGE_GEN=false
```

**Add image generation (when ready):**
```env
IMAGE_MODEL=stable-diffusion
IMAGE_DEVICE=cpu
ENABLE_IMAGE_GEN=true
```

**Add voice assistant:**
```env
ENABLE_VOICE=true
# Install: pip install SpeechRecognition gTTS
```

**Add web search:**
```env
ENABLE_WEB_SEARCH=true
# Install: pip install beautifulsoup4
```

---

## 🧪 Testing Each Feature

### 1. Test Chat AI

```bash
# Using curl
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "user_id": "test"}'

# Using Python
python test_ollama_integration.py

# Using PowerShell
.\test_integration.ps1

# Using browser
# Open: http://localhost:8000/docs
# Try /chat endpoint
```

### 2. Test Image Generation

```python
import requests

response = requests.post('http://localhost:8000/image/generate', json={
    "prompt": "a cute cat wearing a wizard hat",
    "negative_prompt": "blurry, low quality",
    "size": "512x512"
})

print(response.json())
# Image saved to gallery/ folder
```

### 3. Test Voice Assistant

```python
import requests

# Speech to text (need microphone)
stt = requests.post('http://localhost:8000/voice/speech-to-text', json={
    "use_microphone": True
})

# Text to speech
tts = requests.post('http://localhost:8000/voice/text-to-speech', json={
    "text": "Hello, I am Nitro AI assistant"
})

# Audio saved to audio/ folder
```

### 4. Test Web Search

```python
import requests

search = requests.post('http://localhost:8000/search', json={
    "query": "What is machine learning?",
    "summarize": True
})

result = search.json()
print(result['summary'])  # AI summary
print(result['sources'])  # Web sources
```

---

## 🎨 Frontend Setup

### Basic (Already Works):

The frontend works out of the box! Just open `index.html`.

### Advanced (PWA):

To enable mobile app installation:

1. **Add to `index.html` (in `<head>`):**
```html
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#7c3aed">
<link rel="apple-touch-icon" href="icon-192.png">

<!-- Service Worker Registration -->
<script>
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
        .then(reg => console.log('SW registered!', reg))
        .catch(err => console.log('SW registration failed', err));
}
</script>
```

2. **Create icon images:**
   - `icon-192.png` (192x192)
   - `icon-512.png` (512x512)

3. **Test PWA:**
   - Serve over HTTPS (or localhost)
   - Open DevTools → Application → Manifest
   - Check "Service Workers"

---

## 🔧 Troubleshooting

### Issue: Backend won't start

**Solution:**
```bash
# Check Python version
python --version  # Should be 3.11+

# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Try different port
python -m uvicorn main:app --port 8001
```

### Issue: Ollama not connecting

**Solution:**
```bash
# Start Ollama server
ollama serve

# Check if running
curl http://localhost:11434/api/tags

# Pull model again
ollama pull phi3

# Check .env file
# Make sure OLLAMA_BASE_URL=http://localhost:11434
```

### Issue: Image generation fails

**Solution:**
```bash
# Check if installed
pip list | grep diffusers

# Install dependencies
pip install diffusers torch transformers pillow

# For CPU-only (no GPU)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# First generation downloads model (~4GB)
# Be patient, takes 5-10 minutes
```

### Issue: Voice features don't work

**Solution:**
```bash
# Install voice libraries
pip install SpeechRecognition gTTS pyttsx3

# For microphone issues:
# Windows: Download PyAudio wheel (see above)
# macOS: brew install portaudio && pip install pyaudio
# Linux: sudo apt-get install python3-pyaudio portaudio19-dev
```

### Issue: Out of memory

**Solution:**
```env
# Reduce in .env file
AI_MAX_TOKENS=200
IMAGE_MODEL=placeholder
IMAGE_DEVICE=cpu
IMAGE_LOW_MEMORY=true

# Close other applications
# Use smaller AI model
ollama pull phi  # Instead of phi3
```

---

## 📊 Performance Optimization

### For Low-Power Laptops:

```env
# Use smaller models
OLLAMA_MODEL=phi  # 1.6GB instead of phi3 3.8GB

# Reduce token limits
AI_MAX_TOKENS=200

# Disable heavy features
IMAGE_MODEL=placeholder
ENABLE_IMAGE_GEN=false

# Lower temperature
AI_TEMPERATURE=0.3
```

### For Better Quality:

```env
# Use larger models
OLLAMA_MODEL=llama2:13b

# Increase tokens
AI_MAX_TOKENS=1000

# Higher temperature
AI_TEMPERATURE=0.9

# Enable HD images
IMAGE_MODEL=stable-diffusion
IMAGE_DEVICE=cuda  # If you have GPU
```

---

## 🎓 Next Steps

### 1. Customize UI

Edit `frontend/style.css` to change:
- Colors
- Fonts
- Layout
- Animations

### 2. Add Your Own Features

Example: Add custom AI prompt:

```python
# In backend/main.py
@app.post("/custom-chat")
async def custom_chat(message: str):
    response = await chat_ai.generate_response(
        message=message,
        system_prompt="You are a pirate. Always talk like a pirate!"
    )
    return {"response": response}
```

### 3. Connect Database

```bash
pip install sqlalchemy psycopg2-binary

# Add to .env
DATABASE_URL=postgresql://user:pass@localhost:5432/nitroai
```

### 4. Deploy to Cloud

See `DEPLOYMENT_GUIDE.md` for full instructions.

---

## ✅ Success Checklist

- [ ] Python 3.11+ installed
- [ ] Ollama installed and running
- [ ] phi3 model downloaded
- [ ] Backend starts without errors
- [ ] Frontend opens in browser
- [ ] Chat works with real AI responses
- [ ] Image generation tested (or placeholder shown)
- [ ] Voice features tested (or placeholder shown)
- [ ] Web search works
- [ ] All endpoints in `/docs` work
- [ ] PWA manifest configured
- [ ] Service worker registered

---

## 🎉 You're Ready!

Your Nitro AI platform is now fully operational!

### What you have:
✅ **Free** ChatGPT alternative
✅ **Free** image generation (Stable Diffusion)
✅ **Free** voice assistant
✅ **Free** web search AI
✅ Professional UI
✅ Mobile app ready
✅ Deployment ready

### Total monthly cost: **$0!** 🎊

---

## 📚 More Resources

- `README_v5.md` - Feature overview
- `PLATFORM_GUIDE.md` - Complete documentation
- `OLLAMA_INTEGRATION.md` - Ollama setup
- `DEPLOYMENT_GUIDE.md` - Hosting instructions
- `API_REFERENCE.md` - API documentation

---

**Need help?** Check troubleshooting section or read the docs!

**Happy building! 🚀**
