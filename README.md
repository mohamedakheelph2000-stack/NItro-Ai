# 🚀 Nitro AI - Full-Featured AI Assistant Platform

![Version](https://img.shields.io/badge/version-5.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Nitro AI v5.0** is a production-ready, full-featured AI assistant platform with **hybrid AI** (local + cloud), **multi-modal support** (chat, images, voice, search), and **automation agents**. Built for beginners, optimized for laptops, ready for professional deployment!

## ✨ Features at a Glance

| Feature | Status | Description |
|---------|--------|-------------|
| 💬 **Hybrid AI Chat** | ✅ **LIVE** | Ollama (local) + Gemini (cloud) with smart fallback |
| 🎨 **Image Generation** | ✅ **LIVE** | AI-powered text-to-image with gallery |
| 🎤 **Voice Assistant** | ✅ **LIVE** | Speech-to-text + Text-to-speech chat |
| 🔍 **Web Search AI** | ✅ **LIVE** | DuckDuckGo search + AI summaries |
| 🤖 **Automation Agents** | ✅ **NEW!** | Code review, file analysis, task scheduling |
| 📊 **Performance Metrics** | ✅ **NEW!** | Real-time CPU, memory, session monitoring |
| 📱 **Mobile PWA** | ✅ **LIVE** | Install as app, works offline |
| 🐳 **Production Docker** | ✅ **NEW!** | Multi-stage build, orchestration ready |
| 🎥 **Video Search** | 🏗️ **Coming** | YouTube integration with AI recommendations |

---

## 🎯 Quick Start

### Prerequisites

- **Python 3.11+** - [Download here](https://python.org)
- **Git** - [Download here](https://git-scm.com)
- **Ollama** (optional) - [Download here](https://ollama.ai)
- **Docker** (optional) - [Download here](https://docker.com)

### Option 1: Standard Setup (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/nitro-ai.git
cd nitro-ai

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
cd backend
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# Edit .env and add your Gemini API key:
# Get from: https://makersuite.google.com/app/apikey

# 5. Install Ollama (Optional - for local AI)
# Visit https://ollama.ai and install
ollama pull phi3

# 6. Start application
python -m uvicorn main:app --reload

# 7. Open browser → http://localhost:8000
```

### Option 2: Docker Setup (Easiest)

### Option 2: Docker Setup (Easiest)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/nitro-ai.git
cd nitro-ai

# 2. Build image
docker build -f Dockerfile.production -t nitro-ai:latest .

# 3. Run container
docker run -d -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  --name nitro-ai \
  nitro-ai:latest

# 4. Open browser → http://localhost:8000
```

### Option 3: Docker Compose (Production)

```bash
# 1. Clone and configure
git clone https://github.com/yourusername/nitro-ai.git
cd nitro-ai
cp .env.example .env.production
# Edit .env.production with your settings

# 2. Start all services (backend, nginx, redis)
docker-compose -f docker-compose.production.yml up -d

# 3. Check logs
docker-compose logs -f

# 4. Open browser → http://localhost
```

---

## 📖 Documentation

Comprehensive guides to help you succeed:

### 📚 Setup & Configuration
- **[Platform Setup Guide](PLATFORM_SETUP_GUIDE.md)** - Complete setup instructions
- **[Testing Guide](TESTING_GUIDE.md)** - Test all features (800+ lines)

### 🚀 Deployment & Operations
- **[Production Deployment](PRODUCTION_DEPLOYMENT.md)** - Deploy to Render, HuggingFace, AWS, etc.
- **[Performance Optimization](PERFORMANCE_OPTIMIZATION.md)** - Speed optimization guide
- **[Architecture](ARCHITECTURE.md)** - System design and components

### 🛠️ Development
- API Documentation: http://localhost:8000/docs (when running)
- [Contributing Guidelines](#contributing) (below)
- [Troubleshooting](#troubleshooting) (below)

---

## 🏗️ Architecture

```
┌─────────────────────────────┐
│     Frontend (PWA)          │
│  5 Tabs: Chat, Image,       │
│  Voice, Search, Video       │
└────────────┬────────────────┘
             │ REST API
┌────────────▼────────────────┐
│    FastAPI Backend          │
│  • 25+ endpoints            │
│  • Async/await              │
│  • Hybrid AI routing        │
└────────────┬────────────────┘
             │
   ┌─────────┼─────────┐
   │         │         │
┌──▼──┐  ┌──▼──┐  ┌──▼──┐
│Ollama│  │Gemini│  │Agents│
│Local │  │Cloud │  │Code │
│FREE  │  │Fast │  │File │
└─────┘  └─────┘  └─────┘
```

**Key Features**:
- 🤖 **Hybrid AI**: Try Ollama first, fallback to Gemini
- ⚡ **Async**: All operations non-blocking
- 🎨 **Multi-modal**: Text, image, voice, search
- 🤖 **Agents**: Code review, file analysis, automation
- 📊 **Monitoring**: Built-in metrics endpoint
- 🐳 **Docker**: Production-ready containers

👉 See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed diagrams

---

## 🔧 Configuration

Create `backend/.env`:

```env
# ============================================
# NITRO AI v5.0 CONFIGURATION
# ============================================

# Application
APP_NAME=Nitro AI
DEBUG_MODE=false
LOG_LEVEL=INFO

# AI Configuration
AI_MODEL=ollama  # Options: ollama, gemini
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3
GEMINI_API_KEY=your_gemini_api_key_here

# AI Parameters
MAX_TOKENS=500
TEMPERATURE=0.7

# Features (true/false)
ENABLE_IMAGE_GEN=true
ENABLE_VOICE=true
ENABLE_WEB_SEARCH=true
ENABLE_AGENTS=true

# Optional API Keys
HUGGINGFACE_API_KEY=your_hf_key  # For image generation
GOOGLE_CLOUD_API_KEY=your_gc_key  # For voice

# Performance
REDIS_URL=redis://localhost:6379  # Optional caching
RATE_LIMIT_PER_MINUTE=60
```

**Get API Keys**:
- **Gemini**: https://makersuite.google.com/app/apikey (FREE)
- **HuggingFace**: https://huggingface.co/settings/tokens (FREE)

---

## 🚀 Deployment

Deploy Nitro AI to production in minutes!

### FREE Platforms

| Platform | Cost | Ease | Link |
|----------|------|------|------|
| **Render** | FREE 750h | ⭐⭐⭐⭐⭐ | [Guide](PRODUCTION_DEPLOYMENT.md#render-deployment) |
| **HuggingFace** | FREE | ⭐⭐⭐⭐ | [Guide](PRODUCTION_DEPLOYMENT.md#huggingface-deployment) |
| **Replit** | FREE | ⭐⭐⭐⭐⭐ | [Guide](PRODUCTION_DEPLOYMENT.md#replit-deployment) |

### Paid Platforms

| Platform | Cost/Month | Performance |
|----------|-----------|-------------|
| **Railway** | $5-15 | Excellent |
| **Fly.io** | $0-10 | Excellent |
| **DigitalOcean** | $6-12 | Best |

👉 See [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) for step-by-step guides

---

## 🎮 Features Deep Dive

### 💬 Hybrid AI Chat
- **Local-first**: Try Ollama (FREE, private, fast)
- **Cloud fallback**: Gemini if Ollama unavailable
- **Smart context**: Remembers conversation history
- **Model tracking**: Know which AI answered

### 🎨 AI Image Generation
- **Text-to-image**: Generate from descriptions
- **Gallery**: Save all generated images
- **Download**: Export as PNG
- **Styles**: Photorealistic, artistic, anime, etc.

### 🎤 Voice Assistant
- **Speech-to-Text**: Talk to AI
- **Text-to-Speech**: AI talks back
- **Voice chat**: Full hands-free conversation
- **50+ languages**: Multilingual support

### 🔍 Web Search AI
- **DuckDuckGo**: Privacy-focused search
- **AI summaries**: Get answers, not just links
- **Citations**: See sources
- **Current events**: Real-time information

### 🤖 Automation Agents (NEW!)
- **Code Assistant**: Review, analyze, refactor code
- **File Analyzer**: Scan files and directories
- **Task Scheduler**: Automate repetitive tasks
- **Extensible**: Add custom agents easily

### 📊 Performance Monitoring (NEW!)
- **Real-time metrics**: CPU, memory, sessions
- **Health checks**: Automatic monitoring
- **Uptime tracking**: See how long running
- **API endpoint**: `/metrics` for integration

---

## 📡 API Examples

### Chat Message
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "user_id": "user123"}'
```

### Generate Image
```bash
curl -X POST http://localhost:8000/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Mountain sunset",
    "user_id": "user123",
    "width": 512,
    "height": 512
  }'
```

### Code Review (Agent)
```bash
curl -X POST http://localhost:8000/agent/code-review \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    print(\"hi\")",
    "language": "python"
  }'
```

### System Metrics
```bash
curl http://localhost:8000/metrics
```

👉 Full API docs: http://localhost:8000/docs (when running)

---

## 🛠️ Development

### Project Structure

```
nitro-ai/
├── backend/
│   ├── main.py                    # FastAPI app (1100+ lines)
│   ├── ai_router.py              # Hybrid AI routing
│   ├── automation_agents.py      # Agent framework (NEW!)
│   ├── performance_config.py     # Performance settings (NEW!)
│   └── models/ai_modules/
│       ├── image_gen_enhanced.py
│       ├── voice_enhanced.py
│       └── web_search_enhanced.py
│
├── frontend/
│   ├── index.html                # UI with 5 tabs
│   ├── script.js                 # Client logic (900+ lines)
│   ├── style.css                 # Styling (1200+ lines)
│   ├── manifest.json             # PWA config
│   └── sw.js                     # Service worker
│
├── docs/
│   ├── PLATFORM_SETUP_GUIDE.md
│   ├── TESTING_GUIDE.md
│   ├── PRODUCTION_DEPLOYMENT.md  # NEW!
│   ├── PERFORMANCE_OPTIMIZATION.md  # NEW!
│   └── ARCHITECTURE.md           # NEW!
│
├── Dockerfile.production         # NEW! Optimized Docker
├── docker-compose.production.yml # NEW! Orchestration
└── .dockerignore                 # NEW! Build optimization
```

### Tech Stack
- **Backend**: FastAPI, Python 3.11+, Uvicorn
- **Frontend**: Vanilla JS, HTML5, CSS3, PWA
- **AI**: Ollama, Google Gemini, HuggingFace
- **DevOps**: Docker, Docker Compose, Nginx, Redis

---

## 🤝 Contributing

We welcome contributions!

```bash
# 1. Fork & clone
git clone https://github.com/yourusername/nitro-ai.git
cd nitro-ai

# 2. Create branch
git checkout -b feature/your-feature

# 3. Make changes
# ... edit code ...

# 4. Commit & push
git add .
git commit -m "feat: Add awesome feature"
git push origin feature/your-feature

# 5. Create Pull Request
```

**Contribution Ideas**:
- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation
- 🎨 UI improvements
- ⚡ Performance optimizations

---

## 🐛 Troubleshooting

### Ollama Not Connecting
```bash
# Check if running
ollama list

# Start Ollama
ollama serve

# Or use Gemini only
# Set AI_MODEL=gemini in .env
```

### Slow Responses
```bash
# Use smaller model
ollama pull phi3

# Reduce tokens in .env
MAX_TOKENS=300

# Check metrics
curl http://localhost:8000/metrics
```

### Docker Build Fails
```bash
# Clear cache
docker system prune -a

# Rebuild
docker build --no-cache -f Dockerfile.production -t nitro-ai .
```

👉 See [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md) for more tips

---

## 📝 License

MIT License - free for personal and commercial use!

See [LICENSE](LICENSE) for details.

---

## 🌟 Acknowledgments

Built with amazing open-source tools:
- [FastAPI](https://fastapi.tiangolo.com) - Modern Python web framework
- [Ollama](https://ollama.ai) - Run LLMs locally
- [Google Gemini](https://ai.google.dev) - Powerful cloud AI
- [HuggingFace](https://huggingface.co) - ML model hub

Special thanks to the open-source community! ❤️

---

## 📞 Support

- 📖 **Docs**: Start with [PLATFORM_SETUP_GUIDE.md](PLATFORM_SETUP_GUIDE.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/nitro-ai/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/nitro-ai/discussions)

---

## 🗺️ Roadmap

### v5.1 (Next)
- [ ] WebSocket real-time chat
- [ ] User authentication
- [ ] PostgreSQL database
- [ ] Advanced image editing

### v5.2
- [ ] Multi-user support
- [ ] Team collaboration
- [ ] Custom model fine-tuning
- [ ] RAG support

### v6.0 (Future)
- [ ] Mobile apps (iOS/Android)
- [ ] Desktop app
- [ ] Plugin system
- [ ] Multi-agent collaboration

---

<div align="center">

**Made with ❤️ by developers, for developers**

**Nitro AI v5.0** - Your Complete AI Assistant Platform

[⬆ Back to Top](#-nitro-ai---full-featured-ai-assistant-platform)

</div>

### 4️⃣ Start Backend

```bash
cd backend
python run.py
```

### 5️⃣ Open Frontend

Open `frontend/index.html` in your browser!

**🎉 Done! You now have a FREE AI assistant running locally!**

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [PLATFORM_GUIDE.md](PLATFORM_GUIDE.md) | Complete feature guide & API reference |
| [README_v2.md.backup](README_v2.md.backup) | Previous v2.0 documentation |

---

## 🤖 Supported AI Models

### Local (FREE, Private)

- **llama2** (7B) - Best balance → **Recommended for beginners**
- **phi** (2.7B) - Ultra-fast, low RAM
- **mistral** (7B) - High quality
- **codellama** (7B) - Great for code
- **llama2:13b** (13B) - Best quality (needs 8GB RAM)

### Cloud (Paid, API Required)

- OpenAI GPT-4 / GPT-3.5
- Anthropic Claude
- Google Gemini

---

## 💡 Why Nitro AI?

### 🆓 100% Free
- No monthly subscriptions
- No API costs
- No usage limits

### 🔒 Private & Secure
- All data stays on YOUR computer
- No cloud uploads
- Full control

### 🎓 Beginner-Friendly
- Extensive documentation
- Clear code comments
- Easy setup

### 🚀 Production-Ready
- Professional FastAPI backend
- RESTful API design
- Scalable architecture

### 🔧 Extensible
- Modular design
- Plugin system
- Easy to customize

---

## 🛠️ Tech Stack

**Backend:**
- FastAPI (modern Python web framework)
- Pydantic (data validation)
- aiohttp (async HTTP for AI APIs)

**AI:**
- Ollama (local LLM runtime)
- OpenAI/Anthropic (optional cloud APIs)

**Document Generation:**
- ReportLab (PDF)
- python-pptx (PowerPoint)

**Frontend:**
- Vanilla JavaScript (no framework needed!)
- Responsive CSS
- Modern UI

---

## 📊 System Requirements

| Configuration | RAM | Storage | Speed |
|---------------|-----|---------|-------|
| **Minimum** (phi) | 2GB | 2GB | Fast |
| **Recommended** (llama2) | 4GB | 4GB | Great |
| **Optimal** (llama2:13b) | 8GB | 8GB | Best |

---

## 🎓 Usage Examples

### Chat (Normal)

```python
import requests

response = requests.post('http://localhost:8000/chat', json={
    'message': 'What is Python?',
    'user_id': 'user123'
})

print(response.json()['response'])
```

### Chat (Streaming)

```javascript
const response = await fetch('http://localhost:8000/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        message: 'Tell me a story',
        user_id: 'user123'
    })
});

// Read stream word-by-word
const reader = response.body.getReader();
while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    console.log(new TextDecoder().decode(value));
}
```

### Generate PDF

```python
from backend.document_generator import DocumentGenerator

generator = DocumentGenerator()
generator.generate_pdf(
    title="My Report",
    content=["# Introduction", "This is a test report"],
    filename="report.pdf"
)
```

### Detect Language

```python
from backend.language_detector import LanguageDetector

detector = LanguageDetector()
result = detector.detect_language("Bonjour!")
print(result)  # {'language': 'fr', 'language_name': 'French'}
```

---

## 🚀 API Endpoints

### Chat
- `POST /chat` - Standard chat
- `POST /chat/stream` - Streaming chat (SSE)

### Sessions
- `POST /session/create` - New session
- `GET /history/{session_id}` - Get history

### Language
- `POST /language/detect` - Auto-detect language
- `GET /language/supported` - List supported languages

### Documents (Coming Soon)
- `POST /document/pdf` - Generate PDF
- `POST /document/ppt` - Generate PowerPoint

### Video (Architecture Ready)
- `POST /video/generate` - Generate video
- `GET /video/status/{id}` - Check status

---

## 🔧 Configuration

Edit `backend/.env`:

```env
# === AI Settings ===
AI_MODEL=ollama               # ollama, openai, dummy
OLLAMA_MODEL=llama2           # llama2, mistral, phi
OLLAMA_BASE_URL=http://localhost:11434
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=500

# === Features ===
ENABLE_VIDEO_GEN=False
ENABLE_WEB_SEARCH=False
ENABLE_TRANSLATION=False

# === Server ===
DEBUG_MODE=True
PORT=8000
```

---

## 🐛 Troubleshooting

### "Cannot connect to Ollama"

```bash
# Make sure Ollama is running
ollama serve

# Pull the model
ollama pull llama2
```

### "Module not found: aiohttp"

```bash
pip install aiohttp
```

### Port already in use

Change `PORT=8001` in `.env`

---

## 📈 Roadmap

### ✅ v4.0 (Current)
- Local LLM (Ollama)
- Streaming responses
- Document generation
- Multilingual support

### 🔄 v4.1 (Next)
- Web search integration
- Voice AI (STT/TTS)
- Better UI with React

### 📝 v5.0 (Future)
- Agent automation
- Plugin system
- Mobile app
- Docker deployment

---

## 🤝 Contributing

We welcome contributions! Areas needed:

1. **Web Search** - DuckDuckGo/Google integration
2. **Voice AI** - Speech recognition & synthesis
3. **UI** - React/Vue frontend
4. **Testing** - Unit & integration tests
5. **Documentation** - Tutorials & guides

---

## 📄 License

MIT License - Free to use, modify, and distribute!

---

## 🙏 Acknowledgments

Built with amazing open-source tools:
- **Ollama** - Local AI runtime
- **FastAPI** - Modern Python web framework
- **Meta's Llama 2** - Foundation model
- **Mistral AI** - High-quality models

---

## 📞 Support & Community

- 📖 **Documentation:** [PLATFORM_GUIDE.md](PLATFORM_GUIDE.md)
- 🐛 **Issues:** GitHub Issues
- 💬 **Discussions:** GitHub Discussions
- 🌟 **Star this repo** if you find it useful!

---

## 🎯 Perfect For

- 🎓 Students learning AI development
- 💼 Small businesses needing AI tools
- 🔒 Privacy-conscious users
- 🚀 Developers building AI apps
- 💡 Anyone wanting FREE local AI!

---

<div align="center">

**🚀 Start your AI journey with Nitro AI today!**

[Get Started](PLATFORM_GUIDE.md) • [Documentation](PLATFORM_GUIDE.md) • [API Reference](PLATFORM_GUIDE.md#-api-reference)

Made with ❤️ for the open-source community

</div>
