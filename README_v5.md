# 🚀 Nitro AI v5.0 - Complete AI Platform

## ✨ New Features in v5.0

### 1. 🎨 **Image Generation AI**
- Local Stable Diffusion support (FREE!)
- CPU-optimized for laptops
- Generate images from text descriptions
- Gallery with download/save functionality
- Multiple sizes: 512x512, 768x768, 1024x1024
- Customizable quality settings

**How to use:**
```python
# In backend
POST /image/generate
{
    "prompt": "a futuristic city at sunset",
    "negative_prompt": "blurry, low quality",
    "size": "512x512"
}
```

**Requirements:**
```bash
pip install diffusers torch transformers pillow
```

**Note:** First download takes ~4GB. Generation takes 1-3 minutes on CPU.

---

### 2. 🎤 **Voice Assistant**
- Speech-to-Text (microphone or file)
- Text-to-Speech (natural voices)
- Multi-language support
- FREE using Google APIs
- Offline mode with pyttsx3

**How to use:**
```python
# Speech to text
POST /voice/speech-to-text
{"use_microphone": true}

# Text to speech
POST /voice/text-to-speech
{
    "text": "Hello, I am Nitro AI",
    "language": "en"
}
```

**Requirements:**
```bash
pip install SpeechRecognition gTTS pyttsx3
# For microphone: pip install pyaudio
```

---

### 3. 🔍 **Web Search AI** (Perplexity-style)
- Search the web with AI summarization
- Citations and sources included
- FREE using DuckDuckGo
- Processes multiple web pages
- AI-generated summaries

**How to use:**
```python
POST /search
{
    "query": "What is quantum computing?",
    "summarize": true
}
```

**Requirements:**
```bash
pip install aiohttp beautifulsoup4
```

**Response includes:**
- AI summary of results
- Top 5 sources with URLs
- Citations [1], [2], etc.
- Clean extracted content

---

### 4. 🎨 **Enhanced UI**
- Modern ChatGPT-style interface
- Dark mode toggle
- Responsive mobile design
- Multiple tabs (Chat, Image, Voice, Search, Video)
- Professional animations
- Loading states and error handling

---

### 5. 📱 **PWA Support** (Mobile App)
- Progressive Web App enabled
- Install as mobile app
- Works offline (with cache)
- App icon and splash screen
- Native-like experience

---

### 6. 🐳 **Deployment Ready**
- Dockerfile included
- Environment configuration
- Instructions for:
  - Render (free hosting)
  - HuggingFace Spaces
  - Replit
  - Railway
  - Fly.io
- CORS and security configured

---

## 📦 Complete Feature List

### ✅ Already Working (v4.0)
- 💬 Local AI Chat (Ollama phi3)
- 🌐 Multilingual support (10 languages)
- 💾 Conversation memory
- 📝 Document generation (PDF, PPT, TXT)
- 🎬 Video generation (placeholder)
- 📊 Session management
- 🔄 Streaming responses

### ✨ New in v5.0
- 🎨 Image generation (Stable Diffusion)
- 🎤 Voice assistant (STT + TTS)
- 🔍 Web search with AI
- 🌓 Dark mode
- 📱 PWA mobile app
- 🐳 Docker deployment
- 📚 Enhanced documentation

---

## 🚀 Quick Start

### Backend Setup:

```bash
cd backend

# Install all dependencies
pip install fastapi uvicorn aiohttp python-dotenv
pip install diffusers torch transformers pillow  # Image generation
pip install SpeechRecognition gTTS pyttsx3       # Voice assistant
pip install beautifulsoup4                        # Web search

# Start server
python -m uvicorn main:app --reload
```

### Frontend:
```bash
# Open in browser
open frontend/index.html

# Or use Live Server in VS Code
```

### Ollama (for chat):
```bash
# Install from https://ollama.ai
ollama pull phi3
ollama serve
```

---

## 📖 API Endpoints

### Chat
- `POST /chat` - AI chat
- `POST /chat/stream` - Streaming chat

### Image Generation
- `POST /image/generate` - Generate image from prompt
- `GET /image/gallery` - List recent images

### Voice Assistant
- `POST /voice/speech-to-text` - Convert speech to text
- `POST /voice/text-to-speech` - Convert text to speech

### Web Search
- `POST /search` - Search web with AI summary

### Documents
- `POST /document/generate` - Generate PDF/PPT/TXT
- `GET /document/list` - List generated documents

### Video (Placeholder)
- `POST /video/generate` - Generate video (placeholder)
- `GET /video/status/{id}` - Check video status

### System
- `GET /` - API info
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

---

## 🎯 Usage Examples

### 1. Generate Image:
```javascript
const response = await fetch('http://localhost:8000/image/generate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        prompt: "a cat wearing a wizard hat",
        negative_prompt: "blurry, low quality",
        size: "512x512"
    })
});
const data = await response.json();
// data.image_base64 contains the image
```

### 2. Voice Chat:
```javascript
// Speech to text
const sttResponse = await fetch('http://localhost:8000/voice/speech-to-text', {
    method: 'POST',
    body: JSON.stringify({use_microphone: true})
});
const transcript = await sttResponse.json();

// Chat with AI
const chatResponse = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    body: JSON.stringify({
        message: transcript.text,
        user_id: "user123"
    })
});
const aiReply = await chatResponse.json();

// Text to speech
const ttsResponse = await fetch('http://localhost:8000/voice/text-to-speech', {
    method: 'POST',
    body: JSON.stringify({text: aiReply.response})
});
const audio = await ttsResponse.json();
// audio.file_path contains MP3 file
```

### 3. Web Search:
```javascript
const searchResponse = await fetch('http://localhost:8000/search', {
    method: 'POST',
    body: JSON.stringify({
        query: "What is machine learning?",
        summarize: true
    })
});
const results = await searchResponse.json();
// results.summary - AI summary
// results.sources - Web sources with citations
```

---

## 💻 System Requirements

### Minimum (Basic Features):
- CPU: 2 cores
- RAM: 4GB
- Storage: 10GB
- OS: Windows 10+, macOS 10.14+, Linux

### Recommended (All Features):
- CPU: 4+ cores
- RAM: 8GB+ (16GB for image generation)
- Storage: 20GB (for models)
- GPU: NVIDIA 4GB+ VRAM (optional, speeds up image gen)

### Internet:
- Required for: Voice (gTTS), Web Search
- Optional for: Chat (Ollama offline), Image (offline after download)

---

## 🔧 Configuration

### Environment Variables (.env):

```env
# AI Model
AI_MODEL=ollama
OLLAMA_MODEL=phi3
OLLAMA_BASE_URL=http://localhost:11434
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=500

# Image Generation
IMAGE_MODEL=placeholder  # Change to "stable-diffusion" when ready
IMAGE_DEVICE=cpu         # or "cuda" for GPU
IMAGE_LOW_MEMORY=true

# Voice Assistant
VOICE_STT_ENGINE=google
VOICE_TTS_ENGINE=gtts
VOICE_LANGUAGE=en

# Web Search
WEB_SEARCH_MAX_RESULTS=5
WEB_SEARCH_TIMEOUT=10

# Server
HOST=0.0.0.0
PORT=8000
DEBUG_MODE=true
```

---

## 📚 Documentation Files

- `README.md` - Main guide (this file)
- `PLATFORM_GUIDE.md` - Complete platform documentation
- `OLLAMA_INTEGRATION.md` - Ollama setup guide
- `INTEGRATION_COMPLETE.md` - Quick start guide
- `DEPLOYMENT_GUIDE.md` - Hosting instructions
- `PWA_GUIDE.md` - Mobile app setup
- `API_REFERENCE.md` - Complete API documentation

---

## 🐛 Troubleshooting

### Image Generation Not Working:
```bash
# Check if diffusers installed
pip list | grep diffusers

# Install dependencies
pip install diffusers torch transformers pillow

# First use downloads model (~4GB), be patient
```

### Voice Assistant Not Working:
```bash
# For microphone issues on Windows:
pip install pyaudio
# Or download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

# For Linux:
sudo apt-get install python3-pyaudio portaudio19-dev

# For macOS:
brew install portaudio
pip install pyaudio
```

### Web Search Not Working:
```bash
# Install requirements
pip install aiohttp beautifulsoup4

# Check internet connection
curl https://duckduckgo.com
```

---

## 🚀 Deployment Options

### 1. Render (FREE):
- Push to GitHub
- Connect to Render
- Deploy as Web Service
- See `DEPLOYMENT_GUIDE.md`

### 2. HuggingFace Spaces:
- Upload to HF Spaces
- Free GPU option available
- Great for image generation

### 3. Replit:
- Import GitHub repo
- One-click deploy
- Free tier available

### 4. Docker:
```bash
docker build -t nitro-ai .
docker run -p 8000:8000 nitro-ai
```

---

## 📱 Mobile App (PWA)

### Install on Phone:
1. Open `http://your-server/` in mobile browser
2. Tap "Add to Home Screen"
3. App installs like native app
4. Works offline (cached)

### Features:
- App icon on home screen
- Splash screen
- Fullscreen mode
- Push notifications (future)
- Background sync (future)

---

## 🔒 Security

### Implemented:
- CORS configuration
- Input validation
- Error handling
- Rate limiting (recommended for production)

### Recommended for Production:
```python
# Add API key authentication
# Add rate limiting
# Use HTTPS
# Sanitize user inputs
# Enable security headers
```

---

## 📊 Performance Tips

### For Low-Power Laptops:

1. **Image Generation:**
   - Use 512x512 size (faster)
   - Reduce steps to 20 (vs 50)
   - Enable low_memory mode

2. **AI Chat:**
   - Use phi model instead of phi3 (smaller)
   - Reduce max_tokens to 200
   - Lower temperature for faster responses

3. **Web Search:**
   - Reduce max_results to 3
   - Disable AI summarization if slow

4. **General:**
   - Close background apps
   - Use SSD instead of HDD
   - Monitor RAM usage

---

## 🎓 Learning Resources

### Tutorials:
- `docs/BEGINNER_GUIDE.md` - Start here
- `docs/API_TUTORIAL.md` - API usage
- `docs/CUSTOMIZATION.md` - Modify features

### Videos (Future):
- YouTube setup walkthrough
- Feature demonstrations
- Deployment tutorials

---

## 🤝 Contributing

Want to add features? Here's how:

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

### Ideas for Contributions:
- More AI models
- Additional languages
- UI themes
- Mobile improvements
- Performance optimizations

---

## 📈 Roadmap

### v5.1 (Next):
- [ ] Database integration (PostgreSQL)
- [ ] User authentication
- [ ] Advanced image editing
- [ ] Video generation (real)
- [ ] Multi-user support

### v6.0 (Future):
- [ ] Advanced RAG system
- [ ] Code assistant mode
- [ ] Real-time collaboration
- [ ] API marketplace
- [ ] Plugin system

---

## 💡 Tips & Tricks

### Maximize Performance:
```bash
# Use phi instead of phi3 (faster)
ollama pull phi

# Update .env
OLLAMA_MODEL=phi

# Restart backend
```

### Save Money:
```bash
# All features can work FREE:
# - Ollama (chat) - FREE
# - Stable Diffusion (images) - FREE
# - Google STT/TTS (voice) - FREE
# - DuckDuckGo (search) - FREE

# No API costs! 🎉
```

### Quality vs Speed:
```env
# Faster (lower quality)
AI_TEMPERATURE=0.3
AI_MAX_TOKENS=200
IMAGE_STEPS=20

# Better (slower)
AI_TEMPERATURE=0.9
AI_MAX_TOKENS=1000
IMAGE_STEPS=50
```

---

## 🌟 Success Stories

**You can:**
- Build a FREE ChatGPT alternative
- Create a personal AI assistant
- Generate images without DALL-E costs
- Have voice conversations with AI
- Search the web with AI summaries
- Deploy to the cloud for FREE
- Install as mobile app
- Customize everything!

**All running on your laptop! 🚀**

---

## 📞 Support

### Get Help:
- Check `docs/` folder for guides
- Read troubleshooting section above
- See API docs at `/docs` endpoint
- Review example code in `/examples`

### Common Issues:
- **Port 8000 in use:** Change port in .env
- **Model download slow:** Normal, ~4GB file
- **Out of memory:** Reduce image size/quality
- **Ollama not connecting:** Run `ollama serve`

---

## ✅ Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend opens in browser
- [ ] Ollama installed with phi3
- [ ] Chat works with real AI
- [ ] Image generation tested (or placeholder shown)
- [ ] Voice features tested (or placeholder shown)
- [ ] Web search works
- [ ] Dark mode toggles
- [ ] Mobile-responsive
- [ ] PWA installs on phone

---

## 🎉 Congratulations!

You now have a **complete AI platform** running locally!

### What you built:
✅ ChatGPT-like chat interface
✅ Image generation (like DALL-E)
✅ Voice assistant (like Siri)
✅ Web search AI (like Perplexity)
✅ Document generation
✅ Mobile app (PWA)
✅ Deployment-ready
✅ 100% FREE!

**Total cost: $0/month** 🎊

---

**Built with ❤️ by the Nitro AI team**
**Version 5.0 - February 2026**
