# 🚀 NITRO AI - FREE DEPLOYMENT GUIDE
## 100% Free ChatGPT-Style AI Assistant - No Cloud, No APIs, No Costs

---

## 🌟 **WHAT IS NITRO AI?**

Nitro AI is a **completely free**, **private**, and **local** AI assistant that works like ChatGPT - but runs **100% on your device** using Ollama. 

✅ **No API keys required**  
✅ **No subscriptions or costs**  
✅ **No data sent to the cloud**  
✅ **Works offline after setup**  
✅ **Cross-platform:** Web, Mobile (PWA), Desktop (via Electron)

---

## 📦 **SYSTEM REQUIREMENTS**

### Minimum:
- **RAM:** 8GB (4GB model: llama3.2:1b)
- **Storage:** 2GB free space
- **OS:** Windows, macOS, Linux
- **Internet:** Only for initial setup

### Recommended:
- **RAM:** 16GB+ (larger models)
- **Storage:** 10GB+ (multiple models)
- **GPU:** Optional (speeds up responses)

---

## 🛠️ **QUICK START (5 MINUTES)**

### **Step 1: Install Ollama**

Download and install Ollama for your platform:

**Windows/Mac/Linux:**
```bash
# Visit: https://ollama.com/download
# Or use terminal:

# macOS/Linux:
curl -fsSL https://ollama.com/install.sh | sh

# Windows:
# Download installer from https://ollama.com/download
```

### **Step 2: Pull an AI Model**

Choose a model based on your RAM:

```bash
# Ultra-fast, lightweight (1.3GB) - Perfect for chat
ollama pull llama3.2:1b

# OR - Balanced performance (2.3GB)
ollama pull phi3

# OR - High quality (4.7GB)
ollama pull llama3:8b

# OR - Very capable (4.1GB)
ollama pull mistral
```

### **Step 3: Start Backend**

```bash
# Navigate to project
cd "c:\Nitro AI"

# Install Python dependencies (one-time)
pip install -r backend/requirements.txt

# Start backend server
cd backend
python -m uvicorn main:app --reload --port 8000
```

✅ Backend running at: **http://localhost:8000**

### **Step 4: Start Frontend**

Open a new terminal:

```bash
# Navigate to frontend
cd "c:\Nitro AI\frontend"

# Start simple HTTP server
python -m http.server 3000

# OR use Node.js:
npx serve -l 3000
```

✅ Frontend running at: **http://localhost:3000**

### **Step 5: Open in Browser**

Visit: **http://localhost:3000**

🎉 **You're done!** Nitro AI is now running 100% locally.

---

## 🌐 **DEPLOYMENT OPTIONS**

### **Option 1: Local Development (FREE)**

Perfect for personal use on your own device.

**Pros:**
- 100% free forever
- Complete privacy
- Works offline
- Fastest responses

**Cons:**
- Only accessible from your device
- Requires Ollama running locally

**Use case:** Personal AI assistant on your laptop/desktop

---

### **Option 2: Local Network (FREE)**

Share Nitro AI with devices on your home/office network.

#### **Setup:**

1. **Find your local IP:**
   ```bash
   # Windows
   ipconfig
   # Look for "IPv4 Address" (e.g., 192.168.1.100)
   
   # macOS/Linux
   ifconfig | grep inet
   ```

2. **Start backend with external access:**
   ```bash
   cd backend
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. **Update frontend config:**
   Edit `frontend/config.js`:
   ```javascript
   API_BASE_URL: 'http://YOUR_LOCAL_IP:8000'
   // Example: 'http://192.168.1.100:8000'
   ```

4. **Access from any device on your network:**
   - Phone: `http://YOUR_LOCAL_IP:3000`
   - Tablet: `http://YOUR_LOCAL_IP:3000`  
   - Another PC: `http://YOUR_LOCAL_IP:3000`

**Use case:** Family/team AI assistant shared across home network

---

### **Option 3: Web App Deployment (FREE)**

Deploy frontend globally for free, connect to local backend.

#### **Frontend Hosting (Choose One):**

**A. Netlify (Recommended)**
```bash
# 1. Build production ZIP
cd "c:\Nitro AI"
Compress-Archive -Path frontend\* -DestinationPath nitro-ai.zip

# 2. Deploy
# - Go to: app.netlify.com/drop
# - Drag nitro-ai.zip
# - Done! URL: https://YOUR-SITE.netlify.app
```

**B. Vercel**
```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Deploy
cd frontend
vercel

# Result: https://YOUR-PROJECT.vercel.app
```

**C. GitHub Pages**
```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git push origin main

# 2. Enable Pages
# Settings → Pages → Source: main branch → /frontend
# URL: https://YOUR-USERNAME.github.io/nitro-ai
```

#### **Update Frontend Config:**

Edit `frontend/config.js`:
```javascript
// Change this based on your deployment:
API_BASE_URL: 'http://localhost:8000',  // For local testing
// API_BASE_URL: 'http://YOUR_IP:8000',  // For network access
```

**Important:** Backend **must** run on your local device. Free hosting platforms don't support Ollama (requires GPU/RAM).

**Use case:** Access your local AI from anywhere via web browser

---

### **Option 4: Mobile App (PWA - FREE)**

Install Nitro AI as a native-like app on your phone.

#### **Setup:**

1. **Deploy frontend** (see Option 3 above)

2. **Open in mobile browser:**
   - Visit your Netlify/Vercel URL
   - Chrome/Safari will show "Install App" prompt

3. **Install:**
   - Android: Tap "Add to Home Screen"
   - iOS: Tap Share → "Add to Home Screen"

4. **Configure backend:**
   - Make sure backend is accessible (see Option 2 for network access)
   - Or use ngrok/tunneling for remote access

**Use case:** Native app experience on mobile devices

---

### **Option 5: Desktop App (Electron - FREE)**

Package as standalone desktop application.

#### **Setup:**

1. **Install Electron dependencies:**
   ```bash
   npm install electron electron-builder
   ```

2. **Create `main.js`:**
   ```javascript
   const { app, BrowserWindow } = require('electron');
   
   function createWindow() {
     const win = new BrowserWindow({
       width: 1200,
       height: 800,
       webPreferences: {
         nodeIntegration: false,
         contextIsolation: true
       }
     });
     
     // Load your app
     win.loadURL('http://localhost:3000');
     
     // OR for production:
     // win.loadFile('frontend/index.html');
   }
   
   app.whenReady().then(createWindow);
   ```

3. **Update `package.json`:**
   ```json
   {
     "name": "nitro-ai-desktop",
     "version": "1.0.0",
     "main": "main.js",
     "scripts": {
       "start": "electron .",
       "build": "electron-builder"
     }
   }
   ```

4. **Run:**
   ```bash
   npm start
   ```

5. **Build for distribution:**
   ```bash
   npm run build
   # Creates installer in dist/
   ```

**Use case:** Standalone desktop application (Windows/Mac/Linux)

---

## 🔧 **CONFIGURATION**

### **Change AI Model**

Edit `backend/.env`:
```bash
# Choose your model:
OLLAMA_MODEL=llama3.2:1b    # Fastest, 1.3GB
OLLAMA_MODEL=phi3          # Balanced, 2.3GB
OLLAMA_MODEL=mistral       # Powerful, 4.1GB
OLLAMA_MODEL=llama3:8b     # Best quality, 4.7GB
```

Restart backend to apply changes.

### **Adjust AI Behavior**

Edit `backend/ai_router.py`:
```python
"options": {
    "num_predict": 800,      # Max response length
    "temperature": 0.7,      # Creativity (0.1-1.0)
    "top_p": 0.9,           # Diversity
    "num_ctx": 2048         # Context window
}
```

### **Theme**

Click the sun/moon icon in the sidebar to toggle light/dark theme.

---

## 📊 **MODEL COMPARISON**

| Model | Size | RAM | Speed | Quality | Best For |
|-------|------|-----|-------|---------|----------|
| llama3.2:1b | 1.3GB | 4GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | Chat, Quick answers |
| phi3 | 2.3GB | 8GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | General purpose |
| mistral | 4.1GB | 8GB | ⚡⚡ | ⭐⭐⭐⭐ | Complex tasks |
| llama3:8b | 4.7GB | 16GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | High-quality responses |

---

## 🐛 **TROUBLESHOOTING**

### **"Ollama AI is not running"**

**Solution:**
```bash
# Start Ollama server
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### **Backend not connecting**

**Check:**
1. Backend is running: `http://localhost:8000/health`
2. Check console for errors
3. Ensure no firewall blocking port 8000

### **Slow responses**

**Optimize:**
1. Use smaller model (llama3.2:1b)
2. Reduce `num_predict` in ai_router.py
3. Close other heavy applications
4. Use GPU acceleration: `ollama pull llama3.2:1b --gpu`

### **Out of memory**

**Solution:**
1. Use smaller model
2. Reduce `num_ctx` (context window)
3. Close browser tabs
4. Restart Ollama

---

## 🌍 **FREE HOSTING LIMITS**

| Service | Bandwidth | Storage | Build Time |
|---------|-----------|---------|------------|
| **Netlify** | 100GB/month | 100GB | 300 min/month |
| **Vercel** | 100GB/month | 100GB | 6000 min/month |
| **GitHub Pages** | 100GB/month | 1GB | N/A (static) |
| **Railway** | 500 hours/month | N/A | $ credit |

All limits are **more than enough** for personal use. All are **100% FREE**.

---

## 📱 **MOBILE SETUP**

### **Connect Mobile to Local Backend:**

1. **Both devices on same WiFi**

2. **Find computer's IP:**
   ```bash
   # Windows: ipconfig
   # Mac/Linux: ifconfig
   ```

3. **Start backend with external access:**
   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

4. **Access from phone:**
   - Browser: `http://YOUR_IP:3000`
   - Install PWA for native experience

---

## 🔐 **PRIVACY & SECURITY**

### **What stays private?**
- ✅ All conversations (stored locally only)
- ✅ AI model runs on your device
- ✅ No data sent to cloud
- ✅ No tracking or analytics

### **What needs internet?**
- ❌ Model download (one-time, ~1-5GB)
- ❌ Ollama installation (one-time)
- ❌ Web deployment (optional)

After setup, Nitro AI works **100% offline**.

---

## 💡 **TIPS & TRICKS**

### **Faster startup:**
```bash
# Preload model on sistem boot
ollama run llama3.2:1b "test" &
```

### **Multiple models:**
```bash
# Pull several models
ollama pull llama3.2:1b
ollama pull phi3
ollama pull mistral

# Switch in .env or via API
```

### **Reduce latency:**
```bash
# Use CPU-optimized model
ollama pull llama3.2:1b-q4_0
```

---

## 📚 **ADDITIONAL RESOURCES**

- **Ollama Models:** https://ollama.com/library
- **Ollama Docs:** https://github.com/ollama/ollama
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **PWA Guide:** https://web.dev/progressive-web-apps

---

## ❓ **FAQ**

**Q: Can I use this commercially?**  
A: Yes! 100% free for personal and commercial use.

**Q: Do I need an API key?**  
A: No! That's the whole point - 100% free, no keys needed.

**Q: Can I deploy backend to cloud?**  
A: Not on free tiers (Ollama needs GPU/RAM). Use local backend + cloud frontend.

**Q: How to update models?**  
A: `ollama pull MODEL_NAME` downloads latest version.

**Q: Is my data safe?**  
A: Yes! Everything runs locally. No data leaves your device.

**Q: Can I run on Raspberry Pi?**  
A: Yes, but use small models (llama3.2:1b) and expect slower responses.

---

## 🎯 **SUMMARY**

| Deployment | Cost | Setup Time | Access | Best For |
|------------|------|------------|--------|----------|
| **Local** | FREE | 5 min | Your device only | Personal use |
| **Network** | FREE | 10 min | Home/office | Family/team |
| **Web App** | FREE | 15 min | Global (frontend) | Remote access |
| **Mobile PWA** | FREE | 10 min | Phone/tablet | On-the-go |
| **Desktop** | FREE | 20 min | Standalone app | Power users |

---

## 🚀 **GET STARTED NOW!**

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull model
ollama pull llama3.2:1b

# 3. Start backend
cd backend
python -m uvicorn main:app --reload

# 4. Start frontend
cd ../frontend
python -m http.server 3000

# 5. Open browser
# http://localhost:3000

# Done! 🎉
```

---

**Made with ❤️ for the open-source community. 100% Free Forever.**
