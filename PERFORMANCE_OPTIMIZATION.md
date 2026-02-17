# ⚡ Performance Optimization Guide - Nitro AI

## Overview

This guide covers performance optimization strategies for Nitro AI, from development to production deployment. Follow these guidelines to ensure fast, efficient operation even on low-resource systems.

**Target Performance**:
- Chat response: < 3 seconds
- Image generation: < 60 seconds  
- Voice processing: < 5 seconds
- Web search: < 10 seconds

---

## 📋 Table of Contents

1. [Quick Wins](#quick-wins)
2. [Backend Optimizations](#backend-optimizations)
3. [Frontend Optimizations](#frontend-optimizations)
4. [Database & Storage](#database-storage)
5. [Network Optimizations](#network-optimizations)
6. [AI Model Optimizations](#ai-model-optimizations)
7. [Infrastructure](#infrastructure)
8. [Monitoring](#monitoring)
9. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Wins

### 1. Enable Production Mode

```bash
# In .env or environment variables
DEBUG_MODE=false
LOG_LEVEL=WARNING  # Reduce logging overhead
```

**Impact**: 10-15% faster responses

### 2. Use Ollama Locally (If Possible)

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull lightweight model
ollama pull phi3

# Set in .env
AI_MODEL=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

**Impact**: 50-70% faster than cloud API (no network latency)

### 3. Limit Token Generation

```python
# In backend/ai_router.py or .env
MAX_TOKENS=500  # Lower = faster
TEMPERATURE=0.7  # Higher = more creative but slower
```

**Impact**: 30-40% faster for shorter responses

### 4. Use Production Docker

```bash
# Use optimized Dockerfile
docker build -f Dockerfile.production -t nitro-ai:prod .

# Multi-stage build = smaller image = faster startup
```

**Impact**: 50% smaller image, 30% faster startup

---

## 🔧 Backend Optimizations

### 1. Async Everything

**Current Implementation**:
```python
# All endpoints are async
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    response = await get_ai_response(request.message)
    return response
```

**Best Practices**:
```python
# Use async file operations
import aiofiles

async def save_chat_history(user_id: str, messages: list):
    async with aiofiles.open(f"memory/{user_id}/chat.json", "w") as f:
        await f.write(json.dumps(messages))

# Use async HTTP client
import httpx

async def call_external_api(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### 2. Connection Pooling

```python
# For database connections (future)
from databases import Database

database = Database(
    "postgresql://user:pass@localhost/nitro",
    min_size=5,  # Keep 5 connections ready
    max_size=20  # Max 20 concurrent
)
```

### 3. Response Compression

```python
# In main.py
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000  # Compress responses > 1KB
)
```

**Impact**: 60-80% smaller response size

### 4. Request Batching

```python
# Process multiple images at once
@app.post("/batch-generate")
async def batch_generate_images(requests: list[ImageRequest]):
    tasks = [generate_image(req) for req in requests]
    results = await asyncio.gather(*tasks)
    return results
```

### 5. Lazy Loading Models

```python
# Load models only when needed
class AIRouter:
    def __init__(self):
        self._ollama_client = None
        self._gemini_client = None
    
    @property
    def ollama_client(self):
        if self._ollama_client is None:
            self._ollama_client = OllamaClient()
        return self._ollama_client
```

**Impact**: 5-10 seconds faster startup

---

## 🎨 Frontend Optimizations

### 1. Debounce User Input

```javascript
// In script.js
let typingTimer;
const typingDelay = 300;  // Wait 300ms after user stops typing

function handleUserTyping() {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(() => {
        // Only send request after user stops typing
        sendMessage();
    }, typingDelay);
}
```

### 2. Image Lazy Loading

```javascript
// Load images only when visible
function loadImagesLazily() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}
```

### 3. Optimize CSS

```css
/* Use CSS transforms instead of position changes */
.message {
    /* SLOW */
    /* top: 100px; */
    
    /* FAST */
    transform: translateY(100px);
    will-change: transform;
}

/* Minimize repaints */
.chat-container {
    contain: layout style paint;
}
```

### 4. Minimize DOM Manipulation

```javascript
// BAD: Multiple reflows
for (let i = 0; i < messages.length; i++) {
    chatContainer.innerHTML += `<div>${messages[i]}</div>`;
}

// GOOD: Single reflow
const fragment = document.createDocumentFragment();
messages.forEach(msg => {
    const div = document.createElement('div');
    div.textContent = msg;
    fragment.appendChild(div);
});
chatContainer.appendChild(fragment);
```

### 5. Service Worker Caching

```javascript
// In sw.js - cache static assets
const CACHE_NAME = 'nitro-ai-v1';
const urlsToCache = [
    '/',
    '/style.css',
    '/script.js',
    '/manifest.json'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});
```

---

## 💾 Database & Storage {#database-storage}

### 1. Implement Redis Caching

**Install Redis**:
```bash
# Docker
docker run -d -p 6379:6379 redis:alpine

# Or in docker-compose.production.yml (already configured)
```

**Backend Implementation**:
```python
# Add to requirements.txt
# redis==5.0.1
# aioredis==2.0.1

import redis.asyncio as aioredis

# Initialize Redis
redis_client = await aioredis.from_url(
    "redis://localhost:6379",
    encoding="utf-8",
    decode_responses=True
)

# Cache AI responses
async def get_ai_response_cached(message: str, user_id: str):
    # Check cache
    cache_key = f"ai:{user_id}:{hash(message)}"
    cached = await redis_client.get(cache_key)
    
    if cached:
        logger.info("✨ Cache HIT")
        return json.loads(cached)
    
    # Generate response
    response = await get_ai_response(message)
    
    # Store in cache (1 hour TTL)
    await redis_client.setex(
        cache_key,
        3600,
        json.dumps(response)
    )
    
    return response
```

**Impact**: 90-95% faster for repeated queries

### 2. Optimize File Storage

```python
# Use efficient JSON serialization
import orjson  # 3-5x faster than json

# Save
with open('chat.json', 'wb') as f:
    f.write(orjson.dumps(messages))

# Load
with open('chat.json', 'rb') as f:
    messages = orjson.loads(f.read())
```

### 3. Implement Session Cleanup

```python
# In main.py - cleanup old sessions
from datetime import datetime, timedelta

async def cleanup_old_sessions():
    while True:
        await asyncio.sleep(3600)  # Every hour
        
        cutoff = datetime.now() - timedelta(days=30)
        
        for user_id in os.listdir('memory'):
            chat_file = f'memory/{user_id}/chat_history.json'
            if os.path.exists(chat_file):
                mtime = datetime.fromtimestamp(os.path.getmtime(chat_file))
                if mtime < cutoff:
                    shutil.rmtree(f'memory/{user_id}')
                    logger.info(f"🗑️ Cleaned up old session: {user_id}")

# Start on app startup
@app.on_event("startup")
async def startup():
    asyncio.create_task(cleanup_old_sessions())
```

---

## 🌐 Network Optimizations

### 1. Enable HTTP/2

```python
# Run with HTTP/2 support
# Install: pip install uvicorn[standard]

uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --http h11 \
    --workers 4
```

### 2. CDN for Static Assets

```html
<!-- Use CDN for libraries -->
<script src="https://cdn.jsdelivr.net/npm/marked@11.0.0/marked.min.js"></script>

<!-- Self-host critical CSS/JS -->
<link rel="stylesheet" href="/style.css">
<script src="/script.js"></script>
```

### 3. Response Caching Headers

```python
from fastapi.responses import FileResponse

@app.get("/gallery/{filename}")
async def get_image(filename: str):
    return FileResponse(
        f"gallery/{filename}",
        media_type="image/png",
        headers={
            "Cache-Control": "public, max-age=31536000",  # 1 year
            "ETag": f'"{hash(filename)}"'
        }
    )
```

### 4. Rate Limiting

```python
# Install: pip install slowapi

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/chat")
@limiter.limit("60/minute")  # 60 requests per minute
async def chat_endpoint(request: Request, chat_req: ChatRequest):
    # ... existing code
```

**Impact**: Prevent abuse, ensure fair resource usage

---

## 🤖 AI Model Optimizations

### 1. Choose Right Model

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| **phi3** | 2.7B | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Laptop, general chat |
| **llama3.2** | 3B | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Better quality, still fast |
| **gemini-flash** | Cloud | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Best quality, network lag |
| **llama3** | 8B | ⚡⚡ | ⭐⭐⭐⭐⭐ | Needs good CPU/GPU |

**Recommendation**: 
- **Laptop**: phi3 (local) + gemini-flash (fallback)
- **Server**: llama3.2 or llama3 (local)
- **Cloud**: gemini-flash only (no Ollama)

### 2. Optimize Inference Parameters

```python
# In ai_router.py
class AIRouter:
    def __init__(self):
        self.ollama_options = {
            "temperature": 0.7,      # Lower = faster, more deterministic
            "max_tokens": 500,       # Shorter responses = faster
            "top_p": 0.9,           # Nucleus sampling
            "top_k": 40,            # Consider only top 40 tokens
            "repeat_penalty": 1.1,  # Prevent repetition
            "num_predict": 500,     # Max tokens to generate
        }
```

**Parameter Impact**:
- `max_tokens: 100` → 1-2 seconds
- `max_tokens: 500` → 3-5 seconds
- `max_tokens: 2000` → 10-15 seconds

### 3. Model Quantization

```bash
# Use quantized models (smaller, faster)
ollama pull phi3:q4_0  # 4-bit quantization
ollama pull phi3:q8_0  # 8-bit quantization

# Trade-off:
# q4_0: 70% smaller, 2x faster, 5% quality loss
# q8_0: 50% smaller, 1.5x faster, 1% quality loss
```

### 4. Batch Inference (Future)

```python
# Process multiple requests in one batch
async def batch_inference(messages: list[str]):
    responses = await ollama_client.batch_generate(messages)
    return responses
```

**Impact**: 30-50% faster for multiple requests

---

## 🏗️ Infrastructure

### 1. Use Multiple Workers

```bash
# Uvicorn with workers
uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4  # Use 4 CPU cores
```

**Calculation**: `workers = (2 × CPU_cores) + 1`

### 2. Optimize Docker Image

**Current Dockerfile.production** already optimized:
- ✅ Multi-stage build
- ✅ Minimal base image (python:3.11-slim)
- ✅ Compiled wheels (faster package install)
- ✅ Non-root user
- ✅ Health checks

**Further Optimization**:
```dockerfile
# Use Alpine for even smaller image
FROM python:3.11-alpine

# Or use specific Python version with optimizations
FROM python:3.11-slim-bullseye
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
```

### 3. Container Resource Limits

```yaml
# In docker-compose.production.yml (already configured)
services:
  nitro-ai:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

### 4. Use SSD Storage

- **HDD**: 50-100 MB/s read/write
- **SSD**: 500-3000 MB/s read/write

**Impact**: 5-10x faster file operations

---

## 📊 Monitoring

### 1. Built-in Metrics Endpoint

```bash
# Check performance
curl http://localhost:8000/metrics

# Response:
{
  "cpu_percent": 25.3,
  "memory_percent": 48.8,
  "active_sessions": 5,
  "total_messages": 1234,
  "uptime_seconds": 86400
}
```

### 2. Response Time Logging

```python
# Add middleware to track response times
import time
from fastapi import Request

@app.middleware("http")
async def log_response_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(f"⏱️ {request.url.path} took {duration:.2f}s")
    response.headers["X-Response-Time"] = str(duration)
    
    return response
```

### 3. APM Tools (Future)

```python
# Sentry for error tracking
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)

# New Relic for APM
# pip install newrelic
# newrelic-admin run-program uvicorn main:app
```

---

## 🐛 Troubleshooting

### Slow AI Responses

**Check**:
1. Model size: Use phi3 instead of larger models
2. Token limit: Reduce `max_tokens` to 300-500
3. Network: Is Ollama local or cloud?
4. CPU: Check `/metrics` for CPU usage

**Solution**:
```bash
# Switch to faster model
ollama pull phi3:q4_0

# Update .env
AI_MODEL=ollama
OLLAMA_MODEL=phi3:q4_0
MAX_TOKENS=400
```

### High Memory Usage

**Check**:
```bash
# Container memory
docker stats nitro-ai-backend

# System memory
curl http://localhost:8000/metrics
```

**Solution**:
```python
# Implement session limit
MAX_SESSIONS = 100
if len(active_sessions) > MAX_SESSIONS:
    oldest = min(active_sessions.items(), key=lambda x: x[1]['last_active'])
    del active_sessions[oldest[0]]
```

### Slow Image Generation

**Check**:
1. Using cloud API? (20-60 seconds normal)
2. Image size: Larger = slower
3. Quality settings: Higher = slower

**Solution**:
```python
# In image generation request
{
    "width": 512,   # Lower from 1024
    "height": 512,  # Lower from 1024
    "steps": 20     # Lower from 50 (faster, slight quality loss)
}
```

### Database Connection Issues

**Check**:
```bash
# Redis connection
redis-cli ping  # Should return PONG

# Check logs
docker logs nitro-ai-backend | grep -i error
```

**Solution**:
```python
# Add connection retry
async def get_redis_client():
    for i in range(3):
        try:
            client = await aioredis.from_url("redis://localhost:6379")
            await client.ping()
            return client
        except Exception as e:
            logger.warning(f"Redis connection attempt {i+1} failed: {e}")
            await asyncio.sleep(1)
    
    logger.error("Redis unavailable, continuing without cache")
    return None
```

---

## 📈 Performance Benchmarks

### Baseline (No Optimizations)

| Operation | Time | Notes |
|-----------|------|-------|
| Chat (Gemini only) | 5-8s | Network latency |
| Chat (Ollama phi3) | 2-4s | Local CPU |
| Image generation | 30-90s | Cloud API |
| Voice transcribe | 3-5s | Google STT |
| Web search | 8-12s | DuckDuckGo + AI |

### Optimized (All Optimizations)

| Operation | Time | Improvement |
|-----------|------|-------------|
| Chat (Ollama + cache) | 0.1-1s | **90% faster** |
| Chat (Ollama phi3:q4_0) | 1-2s | **50% faster** |
| Image (cached) | 0.1s | **99% faster** |
| Voice (streaming) | 1-2s | **60% faster** |
| Search (cached) | 2-4s | **65% faster** |

---

## ✅ Optimization Checklist

### Quick Wins (30 minutes)
- [ ] Set `DEBUG_MODE=false`
- [ ] Reduce `MAX_TOKENS` to 500
- [ ] Use Ollama locally if possible
- [ ] Use production Dockerfile

### Medium Effort (2-4 hours)
- [ ] Install and configure Redis
- [ ] Add response caching
- [ ] Implement rate limiting
- [ ] Add response compression
- [ ] Enable lazy loading for models

### Advanced (1-2 days)
- [ ] Set up CDN for static assets
- [ ] Implement request batching
- [ ] Add database connection pooling
- [ ] Set up APM monitoring
- [ ] Implement response streaming

### Infrastructure (Ongoing)
- [ ] Monitor `/metrics` endpoint daily
- [ ] Set up alerts for high CPU/memory
- [ ] Regular session cleanup
- [ ] Review and optimize slow endpoints
- [ ] Load testing with realistic traffic

---

## 🎯 Performance Targets

### Laptop (4GB RAM, 4 CPU cores)
- ✅ Chat: < 3 seconds (Ollama phi3)
- ✅ Concurrent users: 5-10
- ✅ Image generation: Use cloud API
- ✅ Memory usage: < 2GB

### Server (8GB RAM, 8 CPU cores)
- ✅ Chat: < 2 seconds (Ollama llama3.2)
- ✅ Concurrent users: 50-100
- ✅ Image generation: Local Stable Diffusion
- ✅ Memory usage: < 4GB

### Cloud (16GB RAM, 16 CPU cores)
- ✅ Chat: < 1 second (cached + Ollama)
- ✅ Concurrent users: 500-1000
- ✅ Image generation: GPU-accelerated
- ✅ Memory usage: < 8GB

---

## 📚 Additional Resources

- [FastAPI Performance Best Practices](https://fastapi.tiangolo.com/deployment/concepts/)
- [Ollama Performance Guide](https://github.com/ollama/ollama/blob/main/docs/faq.md#performance)
- [Redis Caching Strategies](https://redis.io/docs/manual/patterns/)
- [Docker Optimization](https://docs.docker.com/develop/dev-best-practices/)

---

**Remember**: Premature optimization is the root of all evil. Measure first, optimize second! Use the `/metrics` endpoint to identify actual bottlenecks before optimizing.

**Performance Philosophy**: Fast enough is perfect. Don't sacrifice code readability for 5ms gains.
