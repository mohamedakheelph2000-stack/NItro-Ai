# 🚀 Nitro AI - Frontend & Backend Quick Start Guide

## ✅ What Was Fixed

### Frontend Issues Resolved:
1. ✅ **Fixed CSS loading** - Changed `style_new.css` → `style.css`
2. ✅ **Fixed JS loading** - Changed `script_new.js` → `script.js`
3. ✅ **Backend URL verified** - Already set to `http://localhost:8000`
4. ✅ **CORS configured** - Backend allows `http://localhost:3000`
5. ✅ **Chat endpoint working** - `/chat` endpoint responds correctly

---

## 🔧 Current Configuration

### Backend
- **URL:** http://localhost:8000
- **API Endpoint:** http://localhost:8000/chat
- **Health Check:** http://localhost:8000/health
- **AI Model:** llama3 (Ollama)
- **CORS:** Allows localhost:3000

### Frontend
- **URL:** http://localhost:3000
- **Config File:** `frontend/config.js`
- **API Base URL:** `http://localhost:8000`
- **Files:** 
  - HTML: `index.html`
  - CSS: `style.css` ✅
  - JS: `script.js` ✅

---

## 🚀 How to Start/Restart Servers

### Option 1: Quick Start (Both Servers)

**Terminal 1 - Backend:**
```powershell
cd "c:\Nitro AI\backend"
$env:PYTHONIOENCODING="utf-8"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```powershell
cd "c:\Nitro AI\frontend"
python -m http.server 3000
```

**Then open:** http://localhost:3000

---

### Option 2: One-Click Start (Windows)

Use the batch file:
```cmd
START-NITRO-AI.bat
```

---

## 🔄 How to Restart Frontend Only

If you make changes to frontend files (HTML, CSS, JS):

1. **Stop frontend server:**
   - Press `Ctrl+C` in the frontend terminal
   - Or: `Get-Process python | Where-Object {$_.CommandLine -like "*http.server*"} | Stop-Process`

2. **Start frontend again:**
   ```powershell
   cd "c:\Nitro AI\frontend"
   python -m http.server 3000
   ```

3. **Refresh browser:** Press `F5` or `Ctrl+R`

**Note:** You DON'T need to restart the backend when changing frontend files!

---

## 🔄 How to Restart Backend Only

If you change backend code (Python files, .env):

1. **Stop backend:**
   - Press `Ctrl+C` in the backend terminal
   - Or: `Get-Process python | Where-Object {$_.CommandLine -like "*uvicorn*"} | Stop-Process`

2. **Start backend again:**
   ```powershell
   cd "c:\Nitro AI\backend"
   $env:PYTHONIOENCODING="utf-8"
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

**Note:** Backend auto-reloads when you save Python files (thanks to `--reload` flag)!

---

## 🛠️ Troubleshooting

### Frontend not loading CSS/JS
**Problem:** Blank page or unstyled page
**Solution:** 
- Check `index.html` lines 23 and 155
- Should be: `style.css` and `script.js` (not `style_new.css`/`script_new.js`)
- Fixed in latest commit ✅

### Cannot connect to backend
**Error:** "❌ Cannot connect to backend. Make sure the server is running..."

**Check:**
```powershell
# 1. Is backend running?
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing

# 2. Is Ollama running?
ollama list

# 3. Check CORS in backend console output:
# Should show: [CORS] Allowed origins: [..., 'http://localhost:3000', ...]
```

**Fix:**
- Start backend: `cd "c:\Nitro AI\backend"; python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
- Start Ollama: `ollama serve` (usually auto-starts)

### Port already in use
**Error:** "Address already in use"

**Fix:**
```powershell
# Kill all Python processes:
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Then restart servers
```

### CORS errors in browser console
**Error:** "CORS policy: No 'Access-Control-Allow-Origin' header..."

**Check backend config:**
```powershell
# Should output localhost:3000 in allowed origins
cd "c:\Nitro AI\backend"
python -c "from config import settings; print(settings._build_origins())"
```

**Fix:** Backend already configured correctly ✅

---

## 🧪 Test the Connection

### 1. Test Backend Health
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
# Expected: Status 200, {"status":"healthy"}
```

### 2. Test Backend /chat
```powershell
$body = '{"message":"Hello!"}'
Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -ContentType "application/json" -Body $body -UseBasicParsing
# Expected: Status 200, {"response":"...", "ai_model":"llama3"}
```

### 3. Test Frontend
Open browser: http://localhost:3000
- Should see: Nitro AI chat interface with ChatGPT-style design
- Type message and press Enter
- Should get AI response from llama3 model

---

## 📁 File Structure Checklist

```
frontend/
├── index.html          ✅ Fixed (loads style.css & script.js)
├── style.css           ✅ Correct filename
├── script.js           ✅ Correct filename
├── config.js           ✅ API_BASE_URL = http://localhost:8000
├── manifest.json       ✅ PWA config
└── sw.js               ✅ Service worker

backend/
├── main.py             ✅ FastAPI app with CORS
├── ai_router.py        ✅ Ollama llama3 integration
├── config.py           ✅ CORS allows localhost:3000
├── .env                ✅ OLLAMA_MODEL=llama3
└── requirements.txt    ✅ Dependencies
```

---

## 🎯 Quick Commands Reference

### Start Both Servers
```powershell
# Terminal 1 (Backend)
cd "c:\Nitro AI\backend"
$env:PYTHONIOENCODING="utf-8"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 (Frontend)
cd "c:\Nitro AI\frontend"
python -m http.server 3000
```

### Stop Servers
```powershell
# Stop all Python processes
Get-Process python | Stop-Process -Force

# Or press Ctrl+C in each terminal
```

### Check Server Status
```powershell
# Backend health
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing

# Frontend
Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing

# Ollama
ollama list
```

### View Console Logs
**Frontend:** Open browser Dev Tools (F12) → Console tab
**Backend:** Check terminal where uvicorn is running

---

## 🌐 Access URLs

- **Frontend (Chat UI):** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Health:** http://localhost:8000/health
- **API Docs:** http://localhost:8000/docs (FastAPI auto-docs)
- **Ollama:** http://localhost:11434

---

## 📊 Status Summary

```
✅ Frontend: Fixed and running on port 3000
✅ Backend: Running on port 8000 with llama3
✅ API Connection: Working correctly
✅ CORS: Configured properly
✅ Chat Endpoint: Responding with AI
✅ CSS/JS: Loading correctly
```

**Everything is working! 🎉**

---

## 💡 Tips

1. **Auto-reload Backend:** Already enabled with `--reload` flag
2. **Browser Caching:** If changes don't appear, hard refresh with `Ctrl+Shift+R`
3. **Check Console:** Always check browser console (F12) for errors
4. **Backend Logs:** Watch the uvicorn terminal for API call logs
5. **Service Worker:** May cache files - disable in Dev Tools → Application → Service Workers if testing

---

**Last Updated:** Successfully tested and working
**Frontend:** http://localhost:3000
**Backend:** http://localhost:8000 (llama3 model)
