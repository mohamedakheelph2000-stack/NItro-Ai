# 🧪 Nitro AI - Hybrid AI Integration Testing Guide

## Overview

This guide helps you test the **Hybrid AI Router System** that intelligently switches between:
1. **Ollama (LOCAL)** - phi3 model, free, private, laptop-friendly
2. **Gemini (CLOUD)** - Google AI API, fallback when Ollama unavailable

---

## Prerequisites

### Required:
- ✅ Python 3.13 installed
- ✅ Backend dependencies: `pip install -r requirements.txt`
- ✅ Ollama installed: https://ollama.com/download

### Optional (for Gemini fallback):
- 🔑 Gemini API Key: https://makersuite.google.com/app/apikey
- 📝 Add to `.env`: `GEMINI_API_KEY=your_key_here`

---

## Test 1: Ollama Running (LOCAL AI) ✅

### Purpose
Verify Nitro AI uses **Ollama phi3** when available (fastest, free, private).

### Steps

#### 1. Start Ollama Server
```bash
# Terminal 1 - Start Ollama
ollama serve
```

Expected output:
```
Listening on 127.0.0.1:11434
```

#### 2. Pull phi3 Model (if not already done)
```bash
# Terminal 2
ollama pull phi3
```

Expected: Downloads ~3.8GB model

#### 3. Start Nitro AI Backend
```bash
# Terminal 3
cd backend
python -m uvicorn main:app --reload
```

Expected output:
```
🚀 Nitro AI v5.0 is starting...
📝 Debug mode: True
🌐 Server will run on 0.0.0.0:8000
💾 Memory system initialized
```

#### 4. Test API Endpoint

**Option A - Using cURL:**
```bash
curl -X POST "http://localhost:8000/chat" ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"Hello, who are you?\", \"user_id\": \"test_user\"}"
```

**Option B - Using Python:**
```python
import requests

response = requests.post('http://localhost:8000/chat', json={
    "message": "Hello, who are you?",
    "user_id": "test_user"
})

print(response.json())
```

**Option C - Using Browser:**
1. Go to: http://localhost:8000/docs
2. Click on `POST /chat`
3. Click "Try it out"
4. Enter test message
5. Click "Execute"

### Expected Response

```json
{
  "session_id": "some-session-id",
  "response": "Hello! I'm Nitro AI...",
  "timestamp": "2026-02-17T10:30:00",
  "status": "success",
  "user_id": "test_user",
  "ai_model": "phi3",
  "ai_source": "ollama_local"
}
```

### Expected Logs

Check Terminal 3 (backend logs):

```
INFO: 🔄 Attempting Ollama local AI (phi3)...
INFO: ✅ Ollama responded successfully (LOCAL AI)
INFO: 📍 Using LOCAL Ollama AI (phi3)
INFO: ✅ AI response generated | Model: phi3 | Source: ollama_local
INFO: 💾 Conversation saved | Session: xxx | Model: phi3
```

### ✅ Success Indicators
- `"ai_source": "ollama_local"` in response
- `"ai_model": "phi3"` in response
- Logs show: "Using LOCAL Ollama AI"
- Response time: 2-10 seconds (depending on laptop)

---

## Test 2: Gemini Fallback (CLOUD AI) ☁️

### Purpose
Verify Nitro AI falls back to **Gemini** when Ollama unavailable.

### Steps

#### 1. Stop Ollama Server
```bash
# Press Ctrl+C in Terminal 1 (where ollama serve is running)
```

#### 2. Configure Gemini API Key

Create/edit `backend/.env`:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

Get free API key: https://makersuite.google.com/app/apikey

#### 3. Backend Should Still Be Running
(Terminal 3 - no restart needed, auto-reloads on .env change)

#### 4. Test API Endpoint

```bash
curl -X POST "http://localhost:8000/chat" ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"What is 2+2?\", \"user_id\": \"test_user\"}"
```

### Expected Response

```json
{
  "session_id": "some-session-id",
  "response": "2 + 2 equals 4.",
  "timestamp": "2026-02-17T10:35:00",
  "status": "success",
  "user_id": "test_user",
  "ai_model": "gemini-pro",
  "ai_source": "gemini_cloud"
}
```

### Expected Logs

```
INFO: 🔄 Attempting Ollama local AI (phi3)...
WARNING: ❌ Ollama not running (connection refused)
INFO: 🌐 Falling back to Gemini API (cloud)...
INFO: ✅ Gemini responded successfully (CLOUD AI)
INFO: ✅ AI response generated | Model: gemini-pro | Source: gemini_cloud
INFO: 💾 Conversation saved | Session: xxx | Model: gemini-pro
```

### ✅ Success Indicators
- `"ai_source": "gemini_cloud"` in response
- `"ai_model": "gemini-pro"` in response
- Logs show: "Falling back to Gemini API"
- Response time: 1-3 seconds (internet speed dependent)

---

## Test 3: Both Services Down (ERROR HANDLING) ❌

### Purpose
Verify graceful error handling when both AI services fail.

### Steps

#### 1. Stop Ollama (if running)
```bash
# Ctrl+C in ollama serve terminal
```

#### 2. Remove/Invalidate Gemini Key

Edit `backend/.env`:
```env
GEMINI_API_KEY=invalid_key_for_testing
```

#### 3. Test API Endpoint

```bash
curl -X POST "http://localhost:8000/chat" ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"Test error handling\", \"user_id\": \"test_user\"}"
```

### Expected Response

```json
{
  "session_id": "some-session-id",
  "response": "🔧 AI services temporarily unavailable.\n\nTo fix:\n1. Start Ollama: Run 'ollama serve' in terminal\n2. Or add GEMINI_API_KEY to .env file\n\nError: Both AI services unavailable...",
  "timestamp": "2026-02-17T10:40:00",
  "status": "success",
  "user_id": "test_user",
  "ai_model": "none",
  "ai_source": "fallback"
}
```

### Expected Logs

```
WARNING: ❌ Ollama not running (connection refused)
WARNING: 🌐 Falling back to Gemini API (cloud)...
ERROR: ❌ Gemini error: Invalid API key
ERROR: ❌ AI router failed: Both AI services unavailable...
```

### ✅ Success Indicators
- `"ai_source": "fallback"` in response
- `"ai_model": "none"` in response
- Response includes helpful error message
- HTTP status: 200 (doesn't crash, degrades gracefully)

---

## Test 4: Performance Optimization (LAPTOP-FRIENDLY) 🚀

### Purpose
Verify AI responses are fast enough for low-compute laptops.

### Metrics

| Scenario | Target Time | Acceptable Time | Action if Slow |
|----------|-------------|-----------------|----------------|
| Ollama (phi3) | 3-5 seconds | < 15 seconds | Reduce `num_predict` in ai_router.py |
| Gemini API | 1-3 seconds | < 10 seconds | Check internet speed |
| Ollama timeout | 30 seconds | 30 seconds | Configured in ai_router.py |

### Test Script

```python
import requests
import time

def test_performance():
    """Test AI response times"""
    
    messages = [
        "Hello!",
        "What is Python?",
        "Write a haiku about AI"
    ]
    
    for msg in messages:
        start = time.time()
        
        response = requests.post('http://localhost:8000/chat', json={
            "message": msg,
            "user_id": "perf_test"
        })
        
        end = time.time()
        duration = end - start
        
        result = response.json()
        print(f"\n{'='*60}")
        print(f"Message: {msg}")
        print(f"Time: {duration:.2f}s")
        print(f"Model: {result.get('ai_model', 'unknown')}")
        print(f"Source: {result.get('ai_source', 'unknown')}")
        print(f"Response: {result['response'][:100]}...")
        
        # Check performance
        if duration > 15:
            print("⚠️ WARNING: Slow response!")
        else:
            print("✅ Performance OK")

if __name__ == "__main__":
    test_performance()
```

Save as `test_performance.py` and run:
```bash
python test_performance.py
```

---

## Test 5: Frontend Integration 🖥️

### Purpose
Verify frontend can display AI responses from both models.

### Steps

#### 1. Open Frontend
```bash
# Open in browser
start frontend/index.html
```

Or use Live Server in VS Code.

#### 2. Test Chat Interface

1. **With Ollama Running:**
   - Type: "Hello!"
   - Check browser DevTools → Network → Response
   - Should see: `"ai_source": "ollama_local"`

2. **Stop Ollama, Test Gemini:**
   - Stop ollama serve
   - Type: "What's 5+5?"
   - Check DevTools → Should see: `"ai_source": "gemini_cloud"`

3. **Check Console Logs:**
   - Open DevTools → Console
   - Should see model info logged
   - No errors in console

### Expected Behavior
- ✅ Chat messages send correctly
- ✅ AI responses appear in chat
- ✅ No JavaScript errors
- ✅ Seamless switching between models (user doesn't notice)

---

## Test 6: API Documentation (SWAGGER UI) 📖

### Purpose
Verify API documentation is accurate and interactive.

### Steps

1. **Open Swagger UI:**
   ```
   http://localhost:8000/docs
   ```

2. **Check ChatResponse Schema:**
   - Click `POST /chat`
   - Expand "Responses" → 200 → "Example Value"
   - Should include `ai_model` and `ai_source` fields

3. **Test Interactively:**
   - Click "Try it out"
   - Enter test message
   - Click "Execute"
   - Check response includes new fields

### ✅ Success Indicators
- Schema shows `ai_model` and `ai_source`
- Interactive testing works
- Example responses are accurate

---

## Troubleshooting Common Issues 🔧

### Issue 1: "Ollama not running"

**Symptoms:**
```
WARNING: ❌ Ollama not running (connection refused)
```

**Solutions:**
1. Start Ollama: `ollama serve`
2. Check if phi3 model installed: `ollama list`
3. If not installed: `ollama pull phi3`
4. Verify port 11434 not blocked by firewall

---

### Issue 2: "Gemini error: Invalid API key"

**Symptoms:**
```json
{
  "response": "Gemini error: GEMINI_API_KEY not configured..."
}
```

**Solutions:**
1. Get API key: https://makersuite.google.com/app/apikey
2. Add to `backend/.env`:
   ```env
   GEMINI_API_KEY=your_key_here
   ```
3. Restart backend (if not auto-reloading)
4. Verify no extra spaces or quotes in .env

---

### Issue 3: Slow Ollama Responses (>15 seconds)

**Symptoms:**
- Ollama takes very long to respond
- Timeout errors

**Solutions:**

Edit `backend/ai_router.py`, reduce token limit:
```python
"num_predict": 200,  # Was 500, reduce for faster response
"num_ctx": 1024      # Was 2048, reduce context window
```

Or use smaller model:
```bash
ollama pull phi3:mini
```

Then update `ai_router.py`:
```python
"model": "phi3:mini",
```

---

### Issue 4: "Both AI services unavailable"

**Symptoms:**
```
Error: Both AI services unavailable...
```

**Solutions:**
1. **Check Ollama:**
   ```bash
   curl http://localhost:11434/api/tags
   ```
   Should return list of models.

2. **Check Gemini:**
   ```bash
   # Test API key
   curl -H "Content-Type: application/json" \
     -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
     "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_KEY"
   ```

3. **Check Logs:**
   - Look for specific error messages
   - Fix the root cause (network, API key, etc.)

---

### Issue 5: Frontend Not Showing Model Info

**Symptoms:**
- Frontend works but doesn't show which AI model was used

**Solutions:**

Update `frontend/script.js` to display model info:
```javascript
// After receiving response
console.log("AI Model:", response.ai_model);
console.log("AI Source:", response.ai_source);

// Optionally show in UI
if (response.ai_source === "ollama_local") {
    // Show "Powered by Local AI" badge
}
```

---

## Performance Optimization Tips 🚀

### For Low-Compute Laptops:

#### 1. Reduce Token Generation
Edit `ai_router.py`:
```python
"num_predict": 200,  # Shorter responses = faster
```

#### 2. Use Smaller Model
```bash
ollama pull phi3:mini  # Even smaller than phi3
```

#### 3. Reduce Context Window
```python
"num_ctx": 1024,  # Less context = faster processing
```

#### 4. Increase Timeout (if needed)
```python
response = requests.post(..., timeout=60)  # Was 30
```

#### 5. Disable Streaming (Already Done)
```python
"stream": False  # Simpler processing
```

---

## Automated Test Suite 🤖

### Full Integration Test

Save as `test_integration.py`:

```python
"""
Full integration test for Nitro AI Hybrid AI Router
Tests: Ollama, Gemini fallback, error handling, performance
"""
import requests
import time
import subprocess
import os


class NitroAITester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.test_results = []
    
    def test_health(self):
        """Test if backend is running"""
        try:
            response = requests.get(f"{self.base_url}/health")
            assert response.status_code == 200
            self.test_results.append(("Health Check", "PASS"))
            return True
        except:
            self.test_results.append(("Health Check", "FAIL - Backend not running"))
            return False
    
    def test_ollama_local(self):
        """Test Ollama local AI"""
        try:
            response = requests.post(f"{self.base_url}/chat", json={
                "message": "Say 'Ollama working' if you can read this",
                "user_id": "test_ollama"
            }, timeout=30)
            
            result = response.json()
            
            if result.get("ai_source") == "ollama_local":
                self.test_results.append(("Ollama Local", "PASS"))
                return True
            else:
                self.test_results.append(("Ollama Local", f"FAIL - Got {result.get('ai_source')}"))
                return False
        except Exception as e:
            self.test_results.append(("Ollama Local", f"FAIL - {str(e)}"))
            return False
    
    def test_gemini_fallback(self):
        """Test Gemini fallback (manual - requires stopping Ollama)"""
        print("\n⚠️ Manual Test: Stop Ollama and press Enter to test Gemini fallback...")
        input()
        
        try:
            response = requests.post(f"{self.base_url}/chat", json={
                "message": "What is 2+2?",
                "user_id": "test_gemini"
            }, timeout=15)
            
            result = response.json()
            
            if result.get("ai_source") == "gemini_cloud":
                self.test_results.append(("Gemini Fallback", "PASS"))
                return True
            else:
                self.test_results.append(("Gemini Fallback", f"Got {result.get('ai_source')}"))
                return False
        except Exception as e:
            self.test_results.append(("Gemini Fallback", f"FAIL - {str(e)}"))
            return False
    
    def test_performance(self):
        """Test response time"""
        start = time.time()
        
        try:
            response = requests.post(f"{self.base_url}/chat", json={
                "message": "Hi!",
                "user_id": "test_perf"
            }, timeout=30)
            
            duration = time.time() - start
            
            if duration < 15:
                self.test_results.append(("Performance", f"PASS ({duration:.2f}s)"))
                return True
            else:
                self.test_results.append(("Performance", f"SLOW ({duration:.2f}s)"))
                return False
        except Exception as e:
            self.test_results.append(("Performance", f"FAIL - {str(e)}"))
            return False
    
    def test_error_handling(self):
        """Test empty message handling"""
        try:
            response = requests.post(f"{self.base_url}/chat", json={
                "message": "",
                "user_id": "test_error"
            })
            
            if response.status_code == 400:
                self.test_results.append(("Error Handling", "PASS"))
                return True
            else:
                self.test_results.append(("Error Handling", f"FAIL - Got {response.status_code}"))
                return False
        except Exception as e:
            self.test_results.append(("Error Handling", f"FAIL - {str(e)}"))
            return False
    
    def run_all_tests(self):
        """Run all tests and display results"""
        print("\n" + "="*60)
        print("🧪 NITRO AI - HYBRID AI INTEGRATION TESTS")
        print("="*60 + "\n")
        
        # Run tests
        self.test_health()
        self.test_ollama_local()
        self.test_performance()
        self.test_error_handling()
        # self.test_gemini_fallback()  # Uncomment for manual Gemini test
        
        # Display results
        print("\n" + "="*60)
        print("📊 TEST RESULTS")
        print("="*60 + "\n")
        
        passed = 0
        for test_name, result in self.test_results:
            status = "✅" if "PASS" in result else "❌"
            print(f"{status} {test_name:20} | {result}")
            if "PASS" in result:
                passed += 1
        
        total = len(self.test_results)
        print(f"\n{'='*60}")
        print(f"Total: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    tester = NitroAITester()
    tester.run_all_tests()
```

Run tests:
```bash
python test_integration.py
```

---

## Checklist: All Tests Passing ✅

- [ ] Test 1: Ollama local AI works
- [ ] Test 2: Gemini fallback works
- [ ] Test 3: Error handling graceful
- [ ] Test 4: Performance acceptable (<15s)
- [ ] Test 5: Frontend integration works
- [ ] Test 6: API docs accurate
- [ ] Logs show correct model usage
- [ ] JSON responses clean and valid
- [ ] No breaking changes to existing features

---

## Quick Reference Commands

```bash
# Start Ollama
ollama serve

# Pull phi3 model
ollama pull phi3

# Start backend
cd backend
python -m uvicorn main:app --reload

# Test API (Windows)
curl -X POST "http://localhost:8000/chat" ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"Hello!\", \"user_id\": \"test\"}"

# Check logs
# Look at Terminal 3 (backend terminal)

# Check API docs
# Open: http://localhost:8000/docs
```

---

## Success Criteria ✅

Your Nitro AI hybrid integration is **successful** if:

1. ✅ Ollama (phi3) works when running → `ai_source: "ollama_local"`
2. ✅ Gemini works when Ollama down → `ai_source: "gemini_cloud"`
3. ✅ Errors handled gracefully → `ai_source: "fallback"`
4. ✅ Logs clearly show which AI responded
5. ✅ Responses are clean JSON with model tracking
6. ✅ Performance acceptable for laptop (<15s)
7. ✅ No breaking changes to memory, sessions, or other features
8. ✅ Frontend works seamlessly with both AI sources

---

**Happy Testing! 🚀**
