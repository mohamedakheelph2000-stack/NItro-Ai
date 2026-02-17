# 🤖 Ollama Integration Guide - Nitro AI

## ✅ What's Already Done

Your Nitro AI backend is **100% integrated** with Ollama! Here's what's configured:

### Current Setup:
- ✅ **Model**: phi3 (you already pulled it!)
- ✅ **Backend**: ChatAI module fully integrated
- ✅ **Config**: .env file created with phi3 settings
- ✅ **Endpoint**: /chat uses real AI (not dummy responses)
- ✅ **Streaming**: /chat/stream for real-time responses
- ✅ **Error Handling**: Graceful fallback if Ollama not running

---

## 🚀 How to Run Everything

### Step 1: Start Ollama Server

**Option A: Ollama Auto-Starts (Usually)**
Ollama typically runs in the background automatically after installation.

**Option B: Start Manually (if needed)**
```bash
# Open a new terminal and run:
ollama serve
```

**Verify Ollama is Running:**
```bash
# Check if Ollama is accessible
curl http://localhost:11434/api/tags

# Or list your models
ollama list
```

You should see `phi3` in the list!

---

### Step 2: Start Nitro AI Backend

```bash
# Navigate to backend folder
cd "c:\Nitro AI\backend"

# Start the server
python -m uvicorn main:app --reload
```

You should see:
```
🚀 Nitro AI Backend v4.0 is starting...
💾 Memory system initialized
Uvicorn running on http://127.0.0.1:8000
```

---

### Step 3: Test the Integration

#### Test 1: Quick API Test (Command Line)

**PowerShell:**
```powershell
$body = @{
    message = "Hello! Can you introduce yourself in one sentence?"
    user_id = "test_user"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/chat -Method Post -Body $body -ContentType "application/json"
```

**Expected**: Real AI response from phi3 model!

#### Test 2: Interactive API Docs

1. Open browser: **http://localhost:8000/docs**
2. Click on `POST /chat`
3. Click "Try it out"
4. Enter:
   ```json
   {
     "message": "What is Python programming?",
     "user_id": "test_user"
   }
   ```
5. Click "Execute"
6. See **real AI response** below!

#### Test 3: Streaming Chat (Real-time typing effect)

**PowerShell:**
```powershell
$body = @{
    message = "Tell me a short joke"
    user_id = "test_user"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/chat/stream -Method Post -Body $body -ContentType "application/json"
```

**Expected**: Response streams word-by-word like ChatGPT!

#### Test 4: Frontend (Best Experience)

1. Open `frontend/index.html` in your browser
2. Type a message in the chat box
3. Press Send
4. Watch as **phi3 AI generates a real response**!

---

## 🔧 How It Works (Beginner Explanation)

### Architecture Flow:

```
Your Browser (Frontend)
    ↓ HTTP Request
FastAPI Backend (/chat endpoint)
    ↓ Calls ChatAI module
ChatAI Module (chat_ai.py)
    ↓ HTTP Request to localhost:11434
Ollama Server (running phi3 model)
    ↓ AI Generation
phi3 Model (local AI brain!)
    ↓ Response
Back to your browser ✅
```

### What Happens When You Send a Message:

1. **Frontend** sends your message to backend `/chat` endpoint
2. **Backend** receives message, calls `chat_ai.generate_response()`
3. **ChatAI** sends HTTP request to Ollama at `http://localhost:11434/api/chat`
4. **Ollama** loads phi3 model (first time may be slow!)
5. **phi3** generates intelligent response
6. **Response flows back** through ChatAI → Backend → Frontend
7. **You see the AI response!**

### Code Locations:

- **Integration Logic**: `models/ai_modules/chat_ai.py` (450+ lines)
- **Chat Endpoint**: `backend/main.py` (lines 169-208)
- **Streaming Endpoint**: `backend/main.py` (lines 570-630)
- **Configuration**: `backend/.env`

---

## 🎯 Configuration Options

### Switch Models Easily

Edit `backend/.env`:

```env
# Current (phi3 - fast, lightweight)
OLLAMA_MODEL=phi3

# Alternative models you can try:
# OLLAMA_MODEL=llama2        # Balanced quality
# OLLAMA_MODEL=mistral       # High quality
# OLLAMA_MODEL=codellama     # Great for code
# OLLAMA_MODEL=gemma         # Google's model
```

Then restart backend (Ctrl+C, then `python -m uvicorn main:app --reload`)

### Adjust AI Behavior

```env
# Make AI more creative (0.0 = boring, 1.0 = very creative)
AI_TEMPERATURE=0.9

# Make AI more factual
AI_TEMPERATURE=0.3

# Longer responses
AI_MAX_TOKENS=1000

# Shorter responses (saves RAM)
AI_MAX_TOKENS=200
```

---

## 🐛 Troubleshooting

### Problem 1: "Cannot connect to Ollama"

**Symptoms**: Chat returns error about Ollama connection

**Solutions**:
```bash
# Check if Ollama is running
ollama list

# If not running, start it
ollama serve

# Verify it's accessible
curl http://localhost:11434/api/tags
```

**In the chat response**, you'll see:
```
❌ Cannot connect to Ollama. Is it running?

To start Ollama:
1. Install from https://ollama.ai
2. Run: ollama serve
3. Pull a model: ollama pull phi3
```

### Problem 2: First Response Very Slow

**This is NORMAL!** 

- **First message**: 10-30 seconds (phi3 loads into RAM)
- **Subsequent messages**: 1-3 seconds (model already loaded)

**Why?** Ollama loads the 3.8GB phi3 model into memory on first use.

**Tip**: Keep Ollama running in background to avoid reload delays.

### Problem 3: Out of Memory

**Symptoms**: Ollama crashes or very slow

**Solutions**:
1. Close other programs to free RAM
2. Use smaller model:
   ```bash
   ollama pull phi     # Only 1.6GB instead of 3.8GB
   ```
   Then update `.env`:
   ```env
   OLLAMA_MODEL=phi
   ```
3. Reduce response length in `.env`:
   ```env
   AI_MAX_TOKENS=200
   ```

### Problem 4: Backend Returns Dummy Response

**Check**:
1. `.env` file exists in `backend/` folder
2. `.env` has `AI_MODEL=ollama`
3. Backend was restarted after creating .env

**Quick Fix**:
```bash
# Stop backend (Ctrl+C)
# Verify .env exists
cat backend/.env

# Restart backend
cd backend
python -m uvicorn main:app --reload
```

### Problem 5: Response is Gibberish

**Cause**: Model might be corrupted or wrong model pulled

**Solution**:
```bash
# Remove and re-download
ollama rm phi3
ollama pull phi3

# Restart backend
```

---

## 📊 Performance Optimization

### For Low-Power Laptops:

**Option 1: Use Smallest Model (phi)**
```bash
ollama pull phi   # 1.6GB - very fast!
```

Update `.env`:
```env
OLLAMA_MODEL=phi
AI_MAX_TOKENS=200
```

**Option 2: Reduce Context Window**

Edit `backend/main.py` around line 42:
```python
chat_ai = create_chat_ai(
    model_type="ollama",
    config={
        "model": "phi3",
        "max_tokens": 200,  # Shorter responses
        "temperature": 0.7
    }
)
```

**Option 3: Close Background Apps**
- Close Chrome/Edge tabs
- Close other Python processes
- Free up RAM before using AI

---

## 🎨 Frontend Integration

### Your Frontend Already Works!

Open `frontend/index.html` - it's already connected!

**What happens**:
1. User types message
2. Frontend sends to `/chat` endpoint
3. Backend calls Ollama
4. phi3 generates response
5. Response shows in chat!

### Enable Streaming (Optional)

If you want real-time typing effect, modify `frontend/script.js`:

```javascript
// Instead of fetch('/chat'), use:
async function sendMessageStreaming(message) {
    const response = await fetch('/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: message,
            user_id: 'user123'
        })
    });
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        // Display chunk in UI
        appendToChat(chunk);
    }
}
```

---

## 🧪 Advanced Testing

### Test Different Scenarios:

**1. Conversation Context:**
```json
// First message
{"message": "My name is Alice", "user_id": "alice", "session_id": "session1"}

// Second message (should remember)
{"message": "What's my name?", "user_id": "alice", "session_id": "session1"}
```

**2. Multi-language:**
```json
{"message": "Hola, ¿cómo estás?", "user_id": "test"}
```

**3. Technical Questions:**
```json
{"message": "Explain async/await in Python", "user_id": "test"}
```

**4. Creative Tasks:**
```json
{"message": "Write a haiku about coding", "user_id": "test"}
```

---

## 📈 Monitoring

### Check Backend Logs

Watch the terminal where backend runs:

```
[2026-02-17 20:15:23] INFO - Chat request from test_user: Hello!...
[2026-02-17 20:15:24] INFO - Response generated for session xyz123
```

### Check Ollama Logs

```bash
# See what Ollama is doing
ollama logs
```

### Health Check

```bash
# Check backend health
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2026-02-17T20:15:00",
  "version": "4.0.0"
}
```

---

## 🎓 Understanding the Code

### Key File: `models/ai_modules/chat_ai.py`

**Main Functions:**

```python
# Generate response (blocking)
response = await chat_ai.generate_response(
    message="Hello!",
    system_prompt="You are a helpful assistant"
)

# Stream response (word-by-word)
async for chunk in chat_ai.stream_response("Tell me a story"):
    print(chunk, end='', flush=True)

# Clear conversation history
chat_ai.clear_history()
```

### How Ollama Integration Works:

```python
# From chat_ai.py (simplified)
async def generate_response_ollama(self, message: str):
    # Build conversation with history
    messages = []
    for msg in self.conversation_history:
        messages.append(msg)
    messages.append({"role": "user", "content": message})
    
    # Call Ollama HTTP API
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{self.base_url}/api/chat",  # http://localhost:11434/api/chat
            json={
                "model": self.model,      # "phi3"
                "messages": messages,
                "stream": False
            }
        ) as response:
            data = await response.json()
            return data['message']['content']
```

**That's it!** Just HTTP requests to Ollama's local API.

---

## 🎉 Success Checklist

- [ ] Ollama installed and running
- [ ] phi3 model pulled (`ollama list` shows it)
- [ ] `.env` file created in backend/
- [ ] Backend server running (port 8000)
- [ ] Test via `/docs` endpoint - got real AI response
- [ ] Frontend chat working with AI
- [ ] No dummy responses (real phi3 answers!)

---

## 🚀 Next Steps

### 1. Try Different Models
```bash
ollama pull mistral   # Higher quality
ollama pull codellama # For code questions
```

### 2. Enable Streaming in Frontend
See "Frontend Integration" section above

### 3. Add System Prompts
Customize AI personality by editing system_prompt in main.py:

```python
ai_response = await chat_ai.generate_response(
    message=user_text,
    system_prompt="You are Nitro AI, a friendly and helpful coding assistant. Keep answers concise and beginner-friendly."
)
```

### 4. Optimize for Your Use Case
- Coding help? Use `codellama`
- General chat? Use `phi3`
- Best quality? Use `mistral`

---

## 💡 Pro Tips

1. **Keep Ollama Running**: Avoids model reload delays
2. **Use SSD**: Much faster than HDD for model loading
3. **Monitor RAM**: phi3 needs ~4GB free RAM
4. **Start Small**: Use `phi` model first, upgrade later
5. **Cache Responses**: Backend already stores in memory!

---

## 🎯 You're All Set!

Your Nitro AI is now powered by **real AI** running **100% locally** on your computer!

**No costs, no limits, full privacy!** 🔒

Enjoy your FREE AI assistant! 🚀

---

**Need Help?**
- Check backend logs for errors
- Visit http://localhost:8000/docs to test
- Read [PLATFORM_GUIDE.md](../PLATFORM_GUIDE.md) for more
