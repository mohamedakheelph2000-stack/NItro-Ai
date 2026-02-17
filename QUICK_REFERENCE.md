# 🚀 Nitro AI - Quick Reference Card

## ⚡ Quick Start (30 Seconds)

```bash
# 1. Install Ollama
# Download from: https://ollama.ai

# 2. Get AI model
ollama pull llama2

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create config (copy .env.example to .env)
cd backend
cp .env.example .env

# 5. Run!
python run.py

# 6. Open frontend/index.html in browser
```

---

## 🎯 Common Commands

### Ollama Management
```bash
# List models
ollama list

# Pull a model
ollama pull llama2        # Balanced (4GB)
ollama pull phi          # Fast (2GB)
ollama pull mistral      # Quality (4GB)
ollama pull codellama    # For code (4GB)

# Remove a model
ollama rm llama2

# Check if running
ollama serve
```

### Backend Management
```bash
# Start server
cd backend
python run.py

# Or with uvicorn directly
uvicorn main:app --reload --port 8000

# Check health
curl http://localhost:8000/health
```

### Testing
```bash
# Test chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test"}'

# Test streaming
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi", "user_id": "test"}'

# Test language detect
curl -X POST http://localhost:8000/language/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Bonjour"}'
```

---

## 📚 API Endpoints Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Welcome & info |
| `/health` | GET | Health check |
| `/chat` | POST | Standard chat |
| `/chat/stream` | POST | Streaming chat (SSE) |
| `/session/create` | POST | New session |
| `/history/{session_id}` | GET | Get history |
| `/language/detect` | POST | Detect language |
| `/language/supported` | GET | List languages |
| `/video/generate` | POST | Generate video |
| `/video/status/{id}` | GET | Check video status |

---

## 🔧 Configuration Quick Reference

### `.env` File (Minimal)
```env
AI_MODEL=ollama
OLLAMA_MODEL=llama2
DEBUG_MODE=True
PORT=8000
```

### Switch Models
```env
# Fast & lightweight
OLLAMA_MODEL=phi

# High quality
OLLAMA_MODEL=mistral

# For coding
OLLAMA_MODEL=codellama

# Best quality (needs 8GB RAM)
OLLAMA_MODEL=llama2:13b
```

### Adjust AI Behavior
```env
# More creative (fun but random)
AI_TEMPERATURE=0.9

# More factual (boring but accurate)
AI_TEMPERATURE=0.3

# Shorter responses
AI_MAX_TOKENS=200

# Longer responses
AI_MAX_TOKENS=1000
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Cannot connect to Ollama" | Run: `ollama serve` |
| "Module not found: aiohttp" | Run: `pip install aiohttp` |
| "Port already in use" | Change `PORT=8001` in `.env` |
| "Python not found" | Add Python to PATH or use `python3` |
| Slow responses | Use smaller model: `ollama pull phi` |
| Out of memory | Reduce `AI_MAX_TOKENS` or use `phi` |

---

## 📁 File Structure Quick Reference

```
Nitro AI/
├── backend/
│   ├── main.py              # API server
│   ├── config.py            # Settings
│   ├── memory_manager.py    # Conversations
│   ├── language_detector.py # Languages
│   ├── document_generator.py # PDF/PPT ✨NEW
│   ├── .env                 # Your config
│   └── run.py               # Start script
│
├── models/ai_modules/
│   ├── chat_ai.py           # LLM integration ✨NEW
│   └── video_gen.py         # Video (placeholder)
│
├── frontend/
│   ├── index.html           # UI
│   ├── style.css            # Styles
│   └── script.js            # Logic
│
└── docs/
    ├── README.md            # Main docs
    ├── PLATFORM_GUIDE.md    # Complete guide
    ├── SETUP_GUIDE.md       # Installation
    └── CHECKLIST.md         # Verification
```

---

## 🎓 Code Examples

### Python - Chat
```python
import requests

response = requests.post('http://localhost:8000/chat', json={
    'message': 'What is Python?',
    'user_id': 'user123'
})

print(response.json()['response'])
```

### Python - Generate PDF
```python
from backend.document_generator import DocumentGenerator

gen = DocumentGenerator()
gen.generate_pdf(
    title="My Report",
    content=["# Intro", "This is content"],
    filename="report.pdf"
)
```

### JavaScript - Streaming Chat
```javascript
const response = await fetch('http://localhost:8000/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        message: 'Tell me a story',
        user_id: 'user123'
    })
});

const reader = response.body.getReader();
while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    console.log(new TextDecoder().decode(value));
}
```

---

## 🎯 Feature Status

| Feature | Status | Notes |
|---------|--------|-------|
| Local AI (Ollama) | ✅ Live | Free, unlimited |
| Streaming Chat | ✅ Live | Real-time typing |
| Document Gen | ✅ Live | PDF, PPT, TXT |
| Multilingual | ✅ Live | 10 languages |
| Memory System | ✅ Live | Sessions & history |
| Video Gen | 🏗️ Architecture | Ready for APIs |
| Web Search | 📝 Planned | Coming soon |
| Voice AI | 📝 Planned | Coming soon |

---

## 📞 Resources

| Resource | Link |
|----------|------|
| **Ollama** | https://ollama.ai |
| **FastAPI Docs** | https://fastapi.tiangolo.com |
| **Complete Guide** | [PLATFORM_GUIDE.md](PLATFORM_GUIDE.md) |
| **Setup Guide** | [SETUP_GUIDE.md](SETUP_GUIDE.md) |
| **Checklist** | [CHECKLIST.md](CHECKLIST.md) |

---

## 💡 Pro Tips

1. **Save RAM:** Use `phi` model (2GB instead of 4GB)
2. **Speed Up:** Enable GPU in Ollama
3. **Better Quality:** Use `mistral` or `llama2:13b`
4. **Debug:** Set `DEBUG_MODE=True` in `.env`
5. **Privacy:** Ollama = 100% local, no data sent anywhere

---

## 🎉 Quick Wins

### Test in 1 Minute
```bash
# Backend
cd backend && python run.py

# Frontend (new terminal)
cd frontend && python -m http.server 8080
# Open: http://localhost:8080
```

### Switch to Fast Model
```bash
ollama pull phi
# Edit .env: OLLAMA_MODEL=phi
# Restart backend
```

### Generate Your First PDF
```python
from backend.document_generator import DocumentGenerator
gen = DocumentGenerator()
gen.generate_pdf(
    title="Test", 
    content=["Hello World!"], 
    filename="test.pdf"
)
# Check: backend/generated_documents/test.pdf
```

---

**🚀 You're ready to use Nitro AI!**

For detailed help, see: [PLATFORM_GUIDE.md](PLATFORM_GUIDE.md)
