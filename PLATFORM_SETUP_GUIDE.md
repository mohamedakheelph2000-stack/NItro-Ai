# 🚀 Nitro AI Platform - Complete Setup Guide

## Welcome to Your Full-Featured AI Assistant!

Nitro AI is now a comprehensive AI platform with:
- ✅ **Chat AI** - Hybrid Ollama (local) + Gemini (cloud) 
- ✅ **Image Generation** - Stable Diffusion support
- ✅ **Voice Assistant** - Speech-to-text & Text-to-speech
- ✅ **Web Search** - Perplexity-style AI search
- ✅ **Document Generation** - PDF & PPT export
- ✅ **Memory System** - Conversation history
- ✅ **Multi-language** - 10+ languages supported
- ✅ **PWA Ready** - Install as mobile app
- ✅ **Docker Ready** - Deploy to cloud

---

## 📋 Table of Contents

1. [Quick Start (5 minutes)](#quick-start)
2. [Feature-by-Feature Setup](#feature-setup)
3. [Configuration](#configuration)
4. [Testing](#testing)
5. [Deployment](#deployment)
6. [Troubleshooting](#troubleshooting)

---

## 🏃 Quick Start

### Minimum Requirements
- **Python**: 3.10+ (Python 3.13 recommended)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space
- **OS**: Windows, macOS, or Linux

### Basic Installation (Chat Only)

```bash
# 1. Clone or navigate to Nitro AI directory
cd "c:\Nitro AI"

# 2. Install basic dependencies
pip install -r requirements.txt

# 3. Start Ollama (for local AI)
ollama serve

# 4. Pull AI model (in another terminal)
ollama pull phi3

# 5. Start backend
cd backend
python -m uvicorn main:app --reload

# 6. Open frontend
# Open frontend/index.html in your browser
# Or use: start frontend/index.html
```

**That's it! You now have a working AI chat assistant!** 🎉

---

## 🎯 Feature-by-Feature Setup

### 1. Chat AI (Already Working!) ✅

**Status**: ✅ Fully functional out of the box

**Features**:
- Hybrid AI router (Ollama first, Gemini fallback)
- Conversation memory
- Session management
- Multi-language support

**Configuration**:
```env
# backend/.env
AI_MODEL=ollama
OLLAMA_MODEL=phi3
OLLAMA_BASE_URL=http://localhost:11434
```

**Optional - Add Gemini Fallback**:
```env
GEMINI_API_KEY=your_key_here  # Get from https://makersuite.google.com/app/apikey
```

---

### 2. Image Generation 🎨

**Status**: ⚙️ Requires optional libraries

**Install Dependencies**:
```bash
pip install diffusers torch transformers pillow
```

**Download Time**: ~5-10 minutes (4GB Stable Diffusion model)

**Configuration**:
```env
# backend/.env
IMAGE_MODEL=stable-diffusion  # or "placeholder" for demo mode
ENABLE_IMAGE_GEN=true
IMAGE_DEVICE=cpu  # or "cuda" if you have NVIDIA GPU
```

**Usage**:
1. Open frontend
2. Click "Images" tab
3. Enter image description
4. Click "Generate Image"
5. Wait 1-3 minutes (CPU) or 10-30 seconds (GPU)

**Models Available**:
- `runwayml/stable-diffusion-v1-5` (Default, 4GB)
- `CompVis/stable-diffusion-v1-4` (Lightweight, 3GB)
- `stabilityai/stable-diffusion-2-1` (Better quality, 6GB)

**Placeholder Mode** (No installation needed):
- Returns demo images
- Good for testing frontend
- Enable with: `IMAGE_MODEL=placeholder`

---

### 3. Voice Assistant 🎤

**Status**: ⚙️ Requires optional libraries

**Install Dependencies**:
```bash
# Basic voice support
pip install SpeechRecognition gTTS pyttsx3

# Audio input (Windows)
pip install pyaudio

# Audio input (Linux/Mac - if pyaudio fails)
# Linux: sudo apt-get install portaudio19-dev python3-pyaudio
# Mac: brew install portaudio && pip install pyaudio
```

**Configuration**:
```env
# backend/.env
ENABLE_VOICE=true
VOICE_STT_ENGINE=google  # Speech-to-text: google, sphinx
VOICE_TTS_ENGINE=gtts    # Text-to-speech: gtts (online), pyttsx3 (offline)
```

**Usage**:
1. Open frontend
2. Click "Voice" tab
3. Click "Start Recording"
4. Speak your question
5. Click "Stop Recording"
6. AI responds with text and audio

**FREE Services Used**:
- **STT**: Google Web Speech API (FREE, unlimited)
- **TTS**: Google Text-to-Speech (FREE, unlimited)
- **Offline**: pyttsx3 (works without internet)

---

### 4. Web Search 🔍

**Status**: ✅ Works out of the box!

**Dependencies**: Already included (beautifulsoup4, aiohttp)

**Features**:
- DuckDuckGo search (no API key needed!)
- AI-powered summaries
- Citation tracking [1], [2], [3]
- Source links

**Usage**:
1. Open frontend
2. Click "Search" tab
3. Enter your question
4. Get AI summary with sources

**Example Queries**:
- "What's the latest in AI technology?"
- "How to deploy FastAPI to cloud?"
- "Best practices for Python async programming"

**How It Works**:
1. Searches DuckDuckGo (free, no limits)
2. Extracts content from top results
3. Sends to your AI router (Ollama/Gemini)
4. Returns summary with citations

---

### 5. Document Generation 📄

**Status**: ✅ Already working!

**Features**:
- PDF export
- PowerPoint (PPT) export
- Text file export

**Usage**:
- Available in chat interface
- Click export buttons
- Documents saved to `documents/` folder

---

### 6. Video Generation 🎬

**Status**: 🚧 Placeholder (Coming Soon)

**Why Placeholder?**:
- Video generation requires expensive APIs
- RunwayML: ~$0.05-0.10 per 4-second video
- Stable Diffusion Video: Requires high-end GPU

**To Enable (Advanced)**:
1. Get API key from RunwayML or Stable Diffusion
2. Add to `.env`: `VIDEO_API_KEY=your_key`
3. Uncomment code in `models/ai_modules/video_gen.py`
4. See `PLATFORM_GUIDE.md` for details

---

## ⚙️ Configuration

### Complete .env File Example

```env
# === CORE SETTINGS ===
APP_NAME=Nitro AI
VERSION=5.0
DEBUG_MODE=true
HOST=0.0.0.0
PORT=8000

# === AI CONFIGURATION ===
# Primary AI (local, free)
AI_MODEL=ollama
OLLAMA_MODEL=phi3
OLLAMA_BASE_URL=http://localhost:11434
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=500

# Fallback AI (cloud, requires API key)
GEMINI_API_KEY=  # Optional - Get from https://makersuite.google.com/app/apikey

# === IMAGE GENERATION ===
IMAGE_MODEL=placeholder  # Change to "stable-diffusion" when ready
ENABLE_IMAGE_GEN=false   # Set true after installing libraries
IMAGE_DEVICE=cpu         # or "cuda" for NVIDIA GPU
IMAGE_SIZE_DEFAULT=512x512
IMAGE_QUALITY_DEFAULT=standard

# === VOICE ASSISTANT ===
ENABLE_VOICE=true
VOICE_STT_ENGINE=google  # google, sphinx
VOICE_TTS_ENGINE=gtts    # gtts (online), pyttsx3 (offline)
VOICE_LANGUAGE=en

# === WEB SEARCH ===
ENABLE_WEB_SEARCH=true
SEARCH_MAX_RESULTS=5
SEARCH_TIMEOUT=30

# === MEMORY & SESSIONS ===
MAX_MESSAGE_LENGTH=1000
MEMORY_DIR=../memory
LOGS_DIR=../logs

# === CORS (Frontend) ===
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000
```

---

## 🧪 Testing

### Test Each Feature

#### 1. Test Chat
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "user_id": "test"}'
```

Expected: AI response with `"ai_source": "ollama_local"`

#### 2. Test Image Generation
```bash
curl -X POST "http://localhost:8000/image/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a beautiful sunset", "size": "512x512"}'
```

Expected: Base64 image or placeholder message

#### 3. Test Voice (requires libraries)
```bash
# Speech-to-text endpoint exists
curl http://localhost:8000/voice/speech-to-text
```

#### 4. Test Web Search
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Python?", "summarize": true}'
```

Expected: AI summary with sources

### Frontend Testing

1. **Open** `frontend/index.html`
2. **Test tabs**: Chat, Images, Voice, Search, Video
3. **Check console**: No JavaScript errors
4. **Verify API calls**: DevTools → Network tab

---

## 🚀 Deployment

### Option 1: Local Development (Current)
```bash
cd backend
python -m uvicorn main:app --reload
```

### Option 2: Docker (Production)
```bash
# Build image
docker build -t nitro-ai .

# Run container
docker run -p 8000:8000 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 nitro-ai
```

### Option 3: Cloud Platforms

See **DEPLOYMENT_GUIDE.md** for:
- ✅ Render (FREE 750 hours/month)
- ✅ HuggingFace Spaces (FREE with GPU)
- ✅ Replit (One-click deploy)
- ✅ Railway ($5 credit)
- ✅ Fly.io (Global CDN)
- ✅ VPS (DigitalOcean/AWS)

---

## 🔧 Troubleshooting

### Issue 1: "Ollama not running"

**Solution**:
```bash
# Start Ollama server
ollama serve

# Pull model (if not done)
ollama pull phi3
```

### Issue 2: "Module not found: diffusers"

**Solution**:
```bash
pip install diffusers torch transformers pillow
```

Or use placeholder mode:
```env
IMAGE_MODEL=placeholder
```

### Issue 3: "SpeechRecognition not found"

**Solution**:
```bash
pip install SpeechRecognition gTTS pyttsx3
```

### Issue 4: "PyAudio installation fails"

**Windows**:
```bash
pip install pipwin
pipwin install pyaudio
```

**Linux**:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**Mac**:
```bash
brew install portaudio
pip install pyaudio
```

### Issue 5: Slow Image Generation

**Optimize for laptop**:
```env
IMAGE_SIZE_DEFAULT=512x512  # Smaller = faster
IMAGE_DEVICE=cpu
```

Or use smaller model:
```python
# Edit models/ai_modules/image_gen_enhanced.py
model_name = "CompVis/stable-diffusion-v1-4"  # 3GB instead of 4GB
```

### Issue 6: "Connection refused" errors

**Check**:
1. Backend running: `http://localhost:8000/health`
2. Ollama running: `curl http://localhost:11434/api/tags`
3. Firewall not blocking ports 8000 or 11434

### Issue 7: Frontend not loading

**Solutions**:
1. Use Live Server extension in VS Code
2. Or serve with Python:
   ```bash
   cd frontend
   python -m http.server 3000
   ```
3. Open `http://localhost:3000`

---

## 📊 Feature Comparison

| Feature | Status | Free? | Requirements |
|---------|--------|-------|--------------|
| Chat AI | ✅ Working | ✅ Yes | Ollama + phi3 |
| Image Gen | ⚙️ Optional | ✅ Yes | diffusers, torch |
| Voice | ⚙️ Optional | ✅ Yes | SpeechRecognition |
| Web Search | ✅ Working | ✅ Yes | None (built-in) |
| Documents | ✅ Working | ✅ Yes | None (built-in) |
| Video | 🚧 Placeholder | ❌ No | RunwayML API ($) |
| Memory | ✅ Working | ✅ Yes | None (built-in) |
| PWA | ✅ Ready | ✅ Yes | None (built-in) |

---

## 💡 Tips & Best Practices

### 1. Optimize for Your Laptop

**Low RAM (8GB)**:
```env
OLLAMA_MODEL=phi3:mini  # Smaller model
IMAGE_SIZE_DEFAULT=512x512
AI_MAX_TOKENS=200
```

**Medium RAM (16GB)**:
```env
OLLAMA_MODEL=phi3
IMAGE_SIZE_DEFAULT=768x768
AI_MAX_TOKENS=500
```

**High RAM (32GB+)**:
```env
OLLAMA_MODEL=llama2
IMAGE_SIZE_DEFAULT=1024x1024
AI_MAX_TOKENS=1000
```

### 2. Save API Costs

- **Use Ollama** for chat (FREE, unlimited)
- **Use DuckDuckGo** for search (FREE, no API key)
- **Use Google Web Speech** for voice (FREE)
- **Only use Gemini** as fallback when Ollama down

### 3. Speed Up Responses

- Lower `AI_MAX_TOKENS` (fewer words = faster)
- Use `phi3:mini` instead of `phi3`
- Keep image size at 512x512
- Disable features you don't need

### 4. Privacy Tips

- **Ollama = 100% private** (all local, no internet)
- **DuckDuckGo = private search** (no tracking)
- **Gemini = cloud** (data sent to Google)

For maximum privacy: Only use Ollama, disable Gemini.

---

## 🎯 What's Next?

### Immediate Next Steps
1. ✅ Test all features
2. ✅ Configure `.env` for your needs
3. ✅ Install optional dependencies
4. ✅ Customize frontend (colors, branding)

### Future Enhancements
- 🔜 Fine-tune your own models
- 🔜 Add custom AI modules
- 🔜 Deploy to cloud
- 🔜 Enable video generation
- 🔜 Add more languages

---

## 📚 Documentation

- **Quick Reference**: `QUICK_REFERENCE.md`
- **API Documentation**: `http://localhost:8000/docs` (when running)
- **Platform Guide**: `PLATFORM_GUIDE.md`
- **Deployment**: `DEPLOYMENT_GUIDE.md`
- **Testing**: `TESTING_GUIDE.md`
- **Version History**: `VERSION_HISTORY.md`

---

## 🆘 Getting Help

### Common Resources
1. **API Docs**: http://localhost:8000/docs
2. **Logs**: Check `logs/` folder
3. **Console**: Browser DevTools → Console
4. **Backend Logs**: Terminal where uvicorn is running

### Report Issues
- Check existing documentation first
- Look in `logs/app.log` for errors
- Include error messages and steps to reproduce

---

## ✅ Success Checklist

Before deploying, verify:

- [ ] Backend starts without errors
- [ ] Ollama is running and phi3 model loaded
- [ ] Chat works (send message, get response)
- [ ] Image tab loads (even in placeholder mode)
- [ ] Voice tab loads
- [ ] Search works (DuckDuckGo + AI summary)
- [ ] No console errors in frontend
- [ ] All tabs switch correctly
- [ ] API docs accessible at `/docs`
- [ ] Memory persists between sessions

---

**Congratulations! You now have a full-featured AI assistant platform! 🎉**

Cost: **$0/month** (vs commercial alternatives: $40-60/month)

Enjoy your FREE, private, powerful AI assistant!
