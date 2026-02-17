# 🚀 Nitro AI v4.0 - Complete Platform Guide

## 🎯 What is Nitro AI?

Nitro AI is a **full-featured AI platform** similar to ChatGPT, Gemini, and Perplexity - but **FREE, OPEN-SOURCE, and runs LOCALLY** on your laptop!

### ✨ Key Features

1. **💬 Smart Chat with Local LLM**
   - Powered by Ollama (llama2, mistral, phi, etc.)
   - NO monthly fees, NO API costs
   - Streaming responses like ChatGPT
   - Conversation memory & context

2. **🌍 Multilingual Support**
   - Auto-detects 10 languages
   - Support: English, Spanish, French, German, Chinese, Japanese, Arabic, Portuguese, Russian, Italian
   - Pattern-based (no AI needed!)

3. **📄 Document Generation**
   - Create professional PDF reports
   - Generate PowerPoint presentations
   - Export text and Markdown files
   - Built-in templates

4. **🎥 Video Generation Architecture**
   - Ready for Runway, Stable Diffusion, Sora
   - Text-to-video framework
   - Image-to-video support
   - Extensible model system

5. **💾 Advanced Memory System**
   - Multi-session support
   - Conversation history
   - User preferences
   - JSON-based storage (lightweight!)

6. **🔍 Web Search (Coming Soon)**
   - Perplexity-style search
   - Source citations
   - Web scraping ready

7. **🤖 Agent Automation (Planned)**
   - Code generation
   - File analysis
   - Task automation

---

## 🎓 For Beginners - Quick Start

### Step 1: Install Ollama (Local AI)

```bash
# Download from: https://ollama.ai
# Install and run:
ollama pull llama2
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Create .env File

Create `backend/.env`:

```env
# AI Model Settings
AI_MODEL=ollama
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434

# Server Settings
DEBUG_MODE=True
PORT=8000

# Optional Features
ENABLE_VIDEO_GEN=False
ENABLE_WEB_SEARCH=False
```

### Step 4: Start Backend

```bash
cd backend
python run.py
```

### Step 5: Open Frontend

Open `frontend/index.html` in your browser!

---

## 📚 Detailed Documentation

### 🤖 AI Models Supported

#### 1. Ollama (Local, FREE!)

**Recommended for beginners:**
- **llama2** (7B) - Good balance, needs 4GB RAM
- **phi** (2.7B) - Very fast, only 2GB RAM
- **mistral** (7B) - Efficient, great quality

**Advanced models:**
- **llama2:13b** - Better quality (needs 8GB RAM)
- **codellama** - Excellent for code
- **mixtral** - Very powerful (needs 16GB RAM)

**How to switch models:**
```bash
# Pull a new model
ollama pull mistral

# Update .env
AI_MODEL=ollama
OLLAMA_MODEL=mistral
```

#### 2. OpenAI (Cloud, Paid)

```env
AI_MODEL=openai
OPENAI_API_KEY=sk-your-key-here
```

**Cost:** ~$0.002 per message (GPT-3.5)

#### 3. Dummy (Testing)

No AI needed, instant responses for development.

```env
AI_MODEL=dummy
```

---

### 💬 Chat Features

#### Normal Chat

**Endpoint:** `POST /chat`

```javascript
const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        message: "Hello!",
        user_id: "user123",
        session_id: "session-abc"
    })
});
```

#### Streaming Chat (Like ChatGPT!)

**Endpoint:** `POST /chat/stream`

```javascript
const response = await fetch('http://localhost:8000/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        message: "Tell me a story",
        user_id: "user123"
    })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    console.log(chunk); // Display word-by-word!
}
```

---

### 📄 Document Generation

#### Generate PDF

```python
from backend.document_generator import DocumentGenerator

generator = DocumentGenerator()

# Create a professional PDF
generator.generate_pdf(
    title="Project Report",
    content=[
        "## Executive Summary",
        "This report covers...",
        "### Key Findings",
        "- Finding 1",
        "- Finding 2"
    ],
    author="Your Name",
    filename="report.pdf"
)
```

#### Generate PowerPoint

```python
slides = [
    {
        "title": "Introduction",
        "content": ["Welcome", "About this presentation"]
    },
    {
        "title": "Main Points",
        "content": ["Point 1", "Point 2", "Point 3"]
    }
]

generator.generate_ppt(
    title="My Presentation",
    slides=slides,
    filename="presentation.pptx"
)
```

#### API Endpoints (Coming Soon)

- `POST /document/pdf` - Generate PDF
- `POST /document/ppt` - Generate PowerPoint
- `POST /document/text` - Generate text file
- `GET /documents` - List all documents

---

### 🌍 Multilingual Support

#### Auto-Detect Language

```python
from backend.language_detector import LanguageDetector

detector = LanguageDetector()

# Detect language
result = detector.detect_language("Bonjour! Comment allez-vous?")
print(result)  # {'language': 'fr', 'confidence': 0.85, 'language_name': 'French'}
```

#### API Endpoints

- `POST /language/detect` - Detect language
- `GET /language/supported` - List supported languages
- `POST /language/preference` - Set user language preference

---

### 🎥 Video Generation

Currently in placeholder mode. Ready for:
- **Runway ML** - Professional video AI
- **Stable Diffusion Video** - Open-source
- **OpenAI Sora** - When available

```python
from models.ai_modules.video_gen import VideoGenerator

generator = VideoGenerator()

# Generate video (placeholder for now)
result = generator.generate_video(
    prompt="A cat playing piano",
    duration=5,
    resolution="1280x720"
)
```

---

### 💾 Memory System

#### Create Session

```javascript
const session = await fetch('http://localhost:8000/session/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: "user123" })
});
```

#### Get History

```javascript
const history = await fetch('http://localhost:8000/history/session-abc');
```

---

## 🛠️ Advanced Configuration

### Environment Variables (.env)

```env
# === AI MODEL ===
AI_MODEL=ollama
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=500

# === SERVER ===
DEBUG_MODE=True
PORT=8000
HOST=0.0.0.0

# === FEATURES ===
ENABLE_VIDEO_GEN=False
ENABLE_WEB_SEARCH=False
ENABLE_TRANSLATION=False
ENABLE_AUTO_LANGUAGE_DETECT=True

# === LANGUAGE ===
DEFAULT_LANGUAGE=en

# === VIDEO (when enabled) ===
VIDEO_MODEL=none
MAX_VIDEO_DURATION=16
DEFAULT_VIDEO_RESOLUTION=1280x720

# === CLOUD APIs (optional) ===
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
```

---

## 📊 System Requirements

### Minimum (Dummy Mode)
- Python 3.8+
- 2GB RAM
- 500MB disk space

### Recommended (Ollama with phi)
- Python 3.9+
- 4GB RAM
- 2GB disk space
- Modern CPU

### Optimal (Ollama with llama2:13b)
- Python 3.10+
- 8GB RAM
- 5GB disk space
- GPU (optional, but faster)

---

## 🚀 Deployment

### Local Development
```bash
cd backend
python run.py
```

### Production (Uvicorn)
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (Coming Soon)
```dockerfile
FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0"]
```

---

## 🎯 API Reference

### Chat Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Standard chat |
| `/chat/stream` | POST | Streaming chat (SSE) |
| `/session/create` | POST | Create new session |
| `/history/{session_id}` | GET | Get chat history |
| `/history/user/{user_id}` | GET | Get user's sessions |

### Language Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/language/detect` | POST | Detect language |
| `/language/supported` | GET | List languages |
| `/language/preference` | POST | Set preference |

### Video Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/video/generate` | POST | Generate video |
| `/video/status/{task_id}` | GET | Check status |
| `/video/models` | GET | List models |

### System Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome & info |
| `/health` | GET | Health check |
| `/debug/clear-memory` | POST | Clear memory (debug) |

---

## 🧪 Testing

### Test Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "user_id": "test"}'
```

### Test Language Detection
```bash
curl -X POST http://localhost:8000/language/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Hola mundo"}'
```

### Test Health
```bash
curl http://localhost:8000/health
```

---

## 🐛 Troubleshooting

### "Cannot connect to Ollama"

**Solution:**
```bash
# Install Ollama from https://ollama.ai
# Make sure it's running:
ollama serve

# Pull a model:
ollama pull llama2
```

### "Module not found: aiohttp"

**Solution:**
```bash
pip install aiohttp
```

### "PDF generation failed"

**Solution:**
```bash
pip install reportlab python-pptx Pillow
```

### Port 8000 already in use

**Solution:**
```env
# Change port in .env
PORT=8001
```

---

## 🎓 Learning Resources

### For Beginners
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Ollama Guide](https://ollama.ai/library)
- [Python Basics](https://www.python.org/about/gettingstarted/)

### For Advanced Users
- [Async Python](https://realpython.com/async-io-python/)
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [LLM Prompting](https://www.promptingguide.ai/)

---

## 📝 Version History

### v4.0 (Current)
- ✅ Local LLM support (Ollama)
- ✅ Streaming chat responses
- ✅ Document generation (PDF/PPT)
- ✅ Enhanced API with SSE
- 🔄 Web search (in progress)
- 🔄 Agent automation (planned)

### v3.0
- ✅ Multilingual support (10 languages)
- ✅ Video generation architecture
- ✅ Language detection
- ✅ Enhanced frontend with tabs

### v2.0
- ✅ Memory system
- ✅ Multi-session support
- ✅ Conversation history
- ✅ Professional UI

### v1.0
- ✅ Basic chat
- ✅ FastAPI backend
- ✅ Simple frontend

---

## 🤝 Contributing

Nitro AI is open for contributions! Areas we need help:

1. **Web Search Integration** - DuckDuckGo, Google APIs
2. **Voice AI** - Speech-to-text, text-to-speech
3. **Better UI** - React/Vue frontend
4. **More Models** - Claude, Gemini integration
5. **Deployment** - Docker, Kubernetes
6. **Testing** - Unit tests, integration tests

---

## 📄 License

MIT License - Free to use, modify, and distribute!

---

## 🙏 Credits

Built with:
- FastAPI (backend framework)
- Ollama (local AI)
- ReportLab (PDF generation)
- python-pptx (PowerPoint generation)
- Vanilla JS (frontend)

---

## 💡 Tips & Tricks

### Save RAM
Use smaller models like `phi` instead of `llama2:13b`

### Faster Responses
- Use SSD for Ollama models
- Enable GPU acceleration
- Reduce `max_tokens` in .env

### Better Quality
- Increase `temperature` for creative responses
- Use larger models if you have RAM
- Provide more context in system prompts

### Production Ready
1. Set `DEBUG_MODE=False`
2. Use environment secrets
3. Enable rate limiting
4. Add authentication
5. Use HTTPS

---

## 📞 Support

Need help? Check:
1. This documentation
2. Code comments (extensively documented!)
3. GitHub issues
4. Ollama community

---

**🚀 Happy Building with Nitro AI!**
