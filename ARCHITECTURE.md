# 🏗️ Nitro AI - Architecture Documentation

## Overview

Nitro AI is a full-featured AI assistant platform with hybrid AI capabilities, multi-modal support (text, image, voice, search), and production-ready deployment infrastructure.

**Version**: 5.0  
**Architecture**: Microservices-ready monolith with modular design  
**Deployment**: Docker containerized with optional orchestration

---

## 📐 System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   PWA    │  │ Mobile   │  │ Desktop  │  │   API    │       │
│  │  Browser │  │   App    │  │  Client  │  │  Client  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
└───────┼─────────────┼─────────────┼─────────────┼──────────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                          │
                    HTTPS/WSS
                          │
┌─────────────────────────┼─────────────────────────────────────┐
│                   EDGE LAYER (Optional)                        │
│                  ┌──────▼──────┐                              │
│                  │    Nginx    │                              │
│                  │ Reverse     │                              │
│                  │   Proxy     │                              │
│                  └──────┬──────┘                              │
│                         │                                      │
│          ┌──────────────┼──────────────┐                     │
│          │              │              │                      │
│    ┌─────▼─────┐  ┌────▼────┐  ┌─────▼─────┐              │
│    │    SSL    │  │  Rate   │  │   CDN     │              │
│    │Termination│  │ Limit   │  │  Cache    │              │
│    └───────────┘  └─────────┘  └───────────┘              │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────────┐
│                  APPLICATION LAYER                           │
│                  ┌─────▼─────┐                              │
│                  │  FastAPI  │                              │
│                  │   Main    │                              │
│                  │   App     │                              │
│                  └─────┬─────┘                              │
│                        │                                     │
│       ┌───────────────┼───────────────┐                    │
│       │               │               │                     │
│  ┌────▼────┐    ┌────▼────┐    ┌────▼────┐              │
│  │   AI    │    │  Media  │    │Automation│              │
│  │ Router  │    │Processing│    │ Agents  │              │
│  └────┬────┘    └────┬────┘    └────┬────┘              │
│       │              │              │                      │
│  ┌────▼────┐    ┌────▼────┐    ┌────▼────┐              │
│  │ Ollama  │    │ Image   │    │  Code   │              │
│  │ Gemini  │    │ Voice   │    │  File   │              │
│  │         │    │ Search  │    │  Task   │              │
│  └─────────┘    └─────────┘    └─────────┘              │
└─────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────────┐
│                   DATA LAYER                                 │
│       ┌───────────────┼───────────────┐                    │
│       │               │               │                     │
│  ┌────▼────┐    ┌────▼────┐    ┌────▼────┐              │
│  │  Memory │    │  Media  │    │  Logs   │              │
│  │ Sessions│    │ Gallery │    │  Metrics│              │
│  │  (JSON) │    │ (Files) │    │  (JSON) │              │
│  └─────────┘    └─────────┘    └─────────┘              │
│                                                             │
│  ┌──────────────────────────────────────┐                 │
│  │   Redis Cache (Optional)             │                 │
│  │   - Session storage                  │                 │
│  │   - API response cache               │                 │
│  └──────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────────┐
│                EXTERNAL SERVICES                             │
│       ┌───────────────┼───────────────┐                    │
│       │               │               │                     │
│  ┌────▼────┐    ┌────▼────┐    ┌────▼────┐              │
│  │  Ollama │    │  Google │    │DuckDuckGo│              │
│  │  (Local)│    │  Gemini │    │  Search  │              │
│  └─────────┘    └─────────┘    └─────────┘              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 Component Architecture

### 1. Frontend Layer

**Technology**: Vanilla JavaScript, HTML5, CSS3  
**Architecture**: Progressive Web App (PWA)  
**State Management**: In-memory session storage

```
frontend/
├── index.html          # Main UI with 5 tabs
├── script.js           # Client-side logic (900+ lines)
├── style.css           # Responsive styling (1200+ lines)
├── manifest.json       # PWA configuration
└── sw.js              # Service Worker for offline support
```

**Features**:
- **Chat Tab**: Real-time messaging with AI
- **Images Tab**: AI image generation gallery
- **Voice Tab**: Speech-to-text + Text-to-speech
- **Search Tab**: Web search with AI summaries
- **Video Tab**: YouTube search (placeholder)

**Communication**:
- REST API for synchronous requests
- Fetch API with async/await
- WebSocket support (future)

---

### 2. Backend Layer

**Technology**: FastAPI (Python 3.11+)  
**Architecture**: Async, modular design  
**Port**: 8000 (configurable)

```
backend/
├── main.py                    # Main FastAPI app (1100+ lines)
│
├── AI Modules/
│   ├── ai_router.py          # Hybrid AI routing (Ollama → Gemini)
│   ├── gemini_client.py      # Google Gemini integration
│   ├── image_gen_enhanced.py # Image generation (FLUX)
│   ├── voice_enhanced.py     # STT + TTS (Google Cloud)
│   └── web_search_enhanced.py# DuckDuckGo search
│
├── Automation/
│   └── automation_agents.py  # Agent framework
│       ├── CodeAssistantAgent
│       ├── FileAnalyzerAgent
│       └── TaskSchedulerAgent
│
├── Configuration/
│   └── performance_config.py # Performance settings
│
└── Models/
    └── schemas.py            # Pydantic models
```

**Endpoints** (25+):

| Category | Endpoint | Method | Purpose |
|----------|----------|--------|---------|
| **Health** | `/health` | GET | Health check |
| **Chat** | `/chat` | POST | AI conversation |
| **Chat** | `/chat/history/{user_id}` | GET | Get chat history |
| **Chat** | `/chat/clear/{user_id}` | DELETE | Clear history |
| **Image** | `/generate-image` | POST | Generate image |
| **Image** | `/gallery/{user_id}` | GET | Get user gallery |
| **Image** | `/gallery/download/{filename}` | GET | Download image |
| **Voice** | `/voice/transcribe` | POST | Audio → Text |
| **Voice** | `/voice/speak` | POST | Text → Audio |
| **Voice** | `/voice/chat` | POST | Voice conversation |
| **Search** | `/search` | POST | Web search + AI |
| **Video** | `/video/search` | POST | YouTube search |
| **Agents** | `/agent/execute` | POST | Execute agent task |
| **Agents** | `/agent/list` | GET | List agents |
| **Agents** | `/agent/code-review` | POST | Code review |
| **Agents** | `/agent/file-analyze` | POST | File analysis |
| **Metrics** | `/metrics` | GET | System metrics |
| **Static** | `/` | GET | Serve frontend |

---

### 3. AI Router System

**Purpose**: Intelligent routing between local and cloud AI  
**Strategy**: Local-first with cloud fallback

```python
# Flow diagram
User Message
     │
     ▼
AI Router (ai_router.py)
     │
     ├─► Ollama Available? ─► YES ─► Use Ollama (phi3)
     │                              │
     │                              ▼
     │                         Success? ─► Return response
     │                              │
     │                              NO
     │                              │
     └─► Gemini Available? ─► YES ──┘
                              │
                              ▼
                         Use Gemini
                              │
                              ▼
                         Return response
```

**Configuration**:
```python
# Ollama (Local)
- Model: phi3 (2.7B parameters)
- RAM: 4-8GB recommended
- Speed: Fast on laptop CPU
- Cost: FREE

# Gemini (Cloud)
- Model: gemini-1.5-flash
- API: Google AI Studio
- Speed: Medium (network latency)
- Cost: FREE tier generous
```

**Benefits**:
- Privacy: Local AI for sensitive data
- Reliability: Cloud fallback ensures uptime
- Cost: Minimize API costs
- Performance: Local = faster

---

### 4. Automation Agent Framework

**Purpose**: AI-powered automation for code and file operations  
**Architecture**: Modular agent system with routing

```
AgentManager
     │
     ├─► CodeAssistantAgent
     │   ├── analyze_code()
     │   ├── review_code()
     │   └── suggest_refactoring()
     │
     ├─► FileAnalyzerAgent
     │   ├── analyze_file()
     │   └── scan_directory()
     │
     └─► TaskSchedulerAgent
         ├── schedule_task()
         └── list_tasks()
```

**Usage**:
```bash
POST /agent/execute
{
  "task": "review-code",
  "data": {
    "code": "def hello(): print('hi')"
  }
}
```

**Response**:
```json
{
  "agent": "CodeAssistantAgent",
  "result": {
    "analysis": "Code quality good",
    "suggestions": ["Add docstring", "Use f-string"]
  }
}
```

---

## 🔄 Data Flow

### Chat Request Flow

```
1. User types message in frontend
   ↓
2. JavaScript sends POST to /chat
   ↓
3. FastAPI receives request
   ↓
4. AI Router checks Ollama availability
   ↓
5a. If available: Send to Ollama
   ↓
6a. Ollama generates response
   OR
5b. If unavailable: Send to Gemini
   ↓
6b. Gemini generates response
   ↓
7. Save to memory (JSON file)
   ↓
8. Return response to frontend
   ↓
9. JavaScript displays in chat UI
```

### Image Generation Flow

```
1. User enters prompt + settings
   ↓
2. POST to /generate-image
   ↓
3. image_gen_enhanced.py processes
   ↓
4. Call external API (FLUX/Stability)
   ↓
5. Receive image data
   ↓
6. Save to gallery/{user_id}/
   ↓
7. Return image URL
   ↓
8. Frontend displays in gallery
```

### Voice Chat Flow

```
1. User clicks record button
   ↓
2. Browser captures audio (MediaRecorder)
   ↓
3. POST audio to /voice/transcribe
   ↓
4. STT: Audio → Text
   ↓
5. Send text to AI Router
   ↓
6. Get AI response text
   ↓
7. POST text to /voice/speak
   ↓
8. TTS: Text → Audio
   ↓
9. Return audio file
   ↓
10. Frontend plays audio
```

---

## 💾 Data Storage

### File Structure

```
Nitro AI/
├── backend/
│   └── memory/
│       └── {user_id}/
│           └── chat_history.json
│
├── frontend/
│   └── gallery/
│       └── {user_id}/
│           ├── image_001.png
│           ├── image_002.png
│           └── ...
│
└── logs/
    ├── app.log
    ├── error.log
    └── metrics.log
```

### Memory Management

**Chat History**:
```json
{
  "user_id": "12345",
  "messages": [
    {
      "role": "user",
      "content": "Hello!",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help?",
      "timestamp": "2024-01-15T10:30:02Z",
      "ai_model": "ollama",
      "ai_source": "phi3"
    }
  ]
}
```

**Session Storage**:
- In-memory dictionary for active sessions
- Periodic save to disk (every 10 messages)
- Auto-cleanup old sessions (30 days)

---

## 🔒 Security Architecture

### Authentication (Future)
- JWT tokens for API access
- OAuth2 for third-party login
- API key management

### Current Security Measures
1. **CORS**: Configurable allowed origins
2. **Rate Limiting**: Per-user limits (future)
3. **Input Validation**: Pydantic models
4. **File Upload**: Size limits, type checking
5. **Secrets**: Environment variables only
6. **Non-root Docker**: User `nitro:1000`

### Data Privacy
- Local AI = data never leaves server
- Cloud AI = encrypted in transit (HTTPS)
- No persistent user data collection
- User can delete all data via `/chat/clear`

---

## ⚡ Performance Optimizations

### Application Level

1. **Async Operations**:
   - All API endpoints use `async def`
   - Non-blocking I/O for file operations
   - Concurrent AI requests supported

2. **Lazy Loading**:
   - Models loaded on first use
   - Reduce startup time
   - Memory efficient

3. **Caching** (Future):
   - Redis for API responses
   - CDN for static assets
   - Browser caching headers

4. **Response Streaming** (Future):
   - Stream AI responses word-by-word
   - Better UX for long responses
   - Lower perceived latency

### Infrastructure Level

1. **Docker Multi-stage Build**:
   - Compile dependencies in builder stage
   - Copy only wheels to runtime
   - Final image: ~500MB vs 2GB+

2. **Resource Limits**:
   - CPU: 2 cores max
   - Memory: 4GB max
   - Auto-restart on failure

3. **Health Checks**:
   - `/health` endpoint every 30s
   - Container auto-restart if unhealthy
   - Load balancer integration

---

## 📊 Monitoring & Observability

### Built-in Metrics

**Endpoint**: `GET /metrics`

```json
{
  "cpu_percent": 25.3,
  "memory": {
    "total_gb": 16.0,
    "available_gb": 8.2,
    "percent": 48.8
  },
  "sessions": {
    "active": 5,
    "total_messages": 1234
  },
  "uptime_seconds": 86400
}
```

### Logging

**Levels**:
- DEBUG: Development only
- INFO: Normal operations
- WARNING: Potential issues
- ERROR: Failures

**Log Format**:
```
[2024-01-15 10:30:00] INFO 🚀 Starting Nitro AI v5.0
[2024-01-15 10:30:01] INFO 🤖 Ollama connection: SUCCESS
[2024-01-15 10:30:01] INFO 💎 Gemini connection: SUCCESS
[2024-01-15 10:30:05] INFO 💬 Chat request from user_12345
```

### External Monitoring (Recommended)

- **Uptime**: UptimeRobot, Pingdom
- **APM**: Sentry, New Relic (future)
- **Logs**: Papertrail, Logtail

---

## 🚀 Deployment Architecture

### Single Server (Current)

```
┌─────────────────────────────────────┐
│        Single Docker Host           │
│  ┌───────────────────────────────┐ │
│  │     Nitro AI Container        │ │
│  │  ┌─────────┐  ┌─────────┐   │ │
│  │  │FastAPI  │  │ Frontend │   │ │
│  │  │ Backend │  │  Static  │   │ │
│  │  └─────────┘  └─────────┘   │ │
│  │                               │ │
│  │  ┌─────────────────────────┐ │ │
│  │  │   Volumes (Persistent)  │ │ │
│  │  │  - memory/              │ │ │
│  │  │  - gallery/             │ │ │
│  │  │  - logs/                │ │ │
│  │  └─────────────────────────┘ │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Multi-Container (Production)

```
┌─────────────────────────────────────────────────┐
│           Docker Compose Network                │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Nginx   │  │ Nitro AI │  │  Redis   │     │
│  │  Proxy   │─▶│  Backend │─▶│  Cache   │     │
│  │          │  │          │  │          │     │
│  │ Port 80  │  │ Port 8000│  │ Port 6379│     │
│  └──────────┘  └──────────┘  └──────────┘     │
│       │              │              │           │
│  ┌────┴──────────────┴──────────────┴────┐    │
│  │      Shared Volumes Network           │    │
│  │  - memory/  - logs/  - gallery/       │    │
│  └───────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### Scalable (Future)

```
┌────────────────────────────────────────────────┐
│             Load Balancer (Nginx)              │
│                 Port 80/443                     │
└────────┬────────────────────────────────┬──────┘
         │                                 │
    ┌────▼─────┐                      ┌───▼──────┐
    │ Nitro AI │                      │ Nitro AI │
    │Instance 1│                      │Instance 2│
    └────┬─────┘                      └───┬──────┘
         │                                 │
         └────────────┬────────────────────┘
                      │
         ┌────────────▼────────────┐
         │   Shared Services       │
         │  ┌──────────────────┐  │
         │  │ Redis Cluster    │  │
         │  │ (Session Store)  │  │
         │  └──────────────────┘  │
         │  ┌──────────────────┐  │
         │  │  S3 / Storage    │  │
         │  │ (Media Gallery)  │  │
         │  └──────────────────┘  │
         └─────────────────────────┘
```

---

## 🔌 API Architecture

### RESTful Design

**Principles**:
- Resource-based URLs
- HTTP methods (GET, POST, DELETE)
- JSON request/response
- Stateless (except session memory)

**Versioning** (Future):
- `/api/v1/chat`
- `/api/v2/chat` with breaking changes

### Request/Response Format

**Request**:
```json
POST /chat
Content-Type: application/json

{
  "message": "Hello!",
  "user_id": "12345",
  "options": {
    "temperature": 0.7,
    "max_tokens": 500
  }
}
```

**Response**:
```json
200 OK
Content-Type: application/json

{
  "response": "Hi! How can I help you today?",
  "ai_model": "ollama",
  "ai_source": "phi3",
  "timestamp": "2024-01-15T10:30:02Z",
  "session_id": "67890"
}
```

---

## 🧪 Testing Architecture

### Test Pyramid

```
        ┌─────────────┐
        │     E2E     │  ← Selenium (future)
        │   Tests     │
        └─────────────┘
      ┌───────────────────┐
      │  Integration Tests │  ← FastAPI TestClient
      └───────────────────┘
    ┌───────────────────────────┐
    │       Unit Tests          │  ← pytest
    └───────────────────────────┘
```

### Current Testing

**Manual Testing**:
- See `TESTING_GUIDE.md`
- Interactive API docs: `/docs`
- Postman collection (future)

**Automated Testing** (Future):
```
tests/
├── unit/
│   ├── test_ai_router.py
│   ├── test_agents.py
│   └── test_models.py
├── integration/
│   ├── test_chat_api.py
│   └── test_image_api.py
└── e2e/
    └── test_user_flow.py
```

---

## 📈 Scalability Considerations

### Vertical Scaling (Easier)
- Increase CPU cores (2 → 4)
- Increase RAM (4GB → 8GB)
- Faster disk (HDD → SSD)

### Horizontal Scaling (Future)
- Load balancer (Nginx/HAProxy)
- Multiple backend instances
- Shared Redis for sessions
- S3 for media storage
- Database for persistence

### Bottlenecks
1. **AI Inference**: Slowest part
   - Solution: GPU acceleration, model caching
2. **Image Generation**: 20-60s
   - Solution: Queue system, async processing
3. **Memory**: In-memory sessions
   - Solution: Redis, database migration

---

## 🔄 CI/CD Pipeline (Recommended)

```
GitHub Push
     │
     ▼
GitHub Actions
     │
     ├─► Run tests
     │
     ├─► Build Docker image
     │
     ├─► Push to registry
     │
     └─► Deploy to production
         │
         ▼
    Render/Railway/Fly.io
         │
         ▼
    Health check
         │
         ▼
    SUCCESS / ROLLBACK
```

**`.github/workflows/deploy.yml`** (Future):
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker
        run: docker build -f Dockerfile.production .
      - name: Push to Registry
        run: docker push nitro-ai:latest
      - name: Deploy
        run: ./deploy.sh
```

---

## 🎯 Future Architecture Enhancements

### Phase 1: Performance
- [ ] Redis caching layer
- [ ] Response streaming
- [ ] Rate limiting middleware
- [ ] CDN integration

### Phase 2: Features
- [ ] User authentication
- [ ] Multi-user support
- [ ] Real-time WebSocket chat
- [ ] File upload/analysis

### Phase 3: Scale
- [ ] Microservices split
- [ ] Kubernetes deployment
- [ ] Database (PostgreSQL)
- [ ] Message queue (RabbitMQ)

### Phase 4: Advanced AI
- [ ] Custom model fine-tuning
- [ ] Multi-modal fusion
- [ ] Agent collaboration
- [ ] Retrieval-Augmented Generation (RAG)

---

## 📚 Related Documentation

- [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) - Deployment guides
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing procedures
- [PLATFORM_SETUP_GUIDE.md](PLATFORM_SETUP_GUIDE.md) - Setup instructions
- [README.md](README.md) - Quick start

---

**Architecture designed for: Simplicity, Scalability, Maintainability** 🏗️

For questions about architecture decisions, consult this doc or review code comments.
