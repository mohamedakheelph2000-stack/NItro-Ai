# 🎓 Nitro AI - Complete Setup Guide

## For Complete Beginners - Step by Step

This guide assumes **ZERO** programming experience. We'll walk through everything together!

---

## 📋 Prerequisites Check

Before we start, you need:

### 1. **A Computer** 
- Windows, Mac, or Linux
- At least 4GB RAM (8GB recommended)
- 5GB free disk space

### 2. **Python 3.8 or higher**

**Check if you have Python:**

```bash
python --version
```

**Don't have Python?**
- Download from: https://www.python.org/downloads/
- **Windows:** Check "Add Python to PATH" during installation!
- **Mac:** Use Homebrew: `brew install python3`
- **Linux:** `sudo apt install python3 python3-pip`

### 3. **Internet Connection**
- To download Ollama and models
- After setup, works fully offline!

---

## 🚀 Installation Steps

### Step 1: Download Nitro AI

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/yourusername/nitro-ai.git
cd nitro-ai
```

**Option B: Download ZIP**
- Download from GitHub
- Extract to a folder like `C:\Nitro AI` or `~/nitro-ai`
- Open terminal in that folder

---

### Step 2: Install Ollama (Local AI Engine)

Ollama is what makes the AI work locally, for FREE!

#### Windows & Mac

1. **Download:** https://ollama.ai/download
2. **Install:** Run the installer (double-click)
3. **Verify:** Open terminal and run:

```bash
ollama --version
```

You should see something like: `ollama version 0.1.17`

#### Linux

```bash
curl https://ollama.ai/install.sh | sh
```

---

### Step 3: Download an AI Model

Now let's get an AI brain! We'll start with **llama2** (good balance of speed and quality).

**Open terminal and run:**

```bash
ollama pull llama2
```

**This will take 5-10 minutes** (downloading ~4GB). Be patient! ☕

**Alternative models you can try:**
```bash
# Ultra-fast, very lightweight (2GB)
ollama pull phi

# Higher quality, more RAM needed (7GB)
ollama pull mistral

# Best for coding (4GB)
ollama pull codellama
```

**Verify it worked:**
```bash
ollama list
```

You should see your downloaded model!

---

### Step 4: Install Python Dependencies

Navigate to your Nitro AI folder and run:

```bash
cd "c:\Nitro AI"  # Windows
# or
cd ~/nitro-ai     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

**What's happening?**
- Installing FastAPI (web server)
- Installing aiohttp (for AI communication)
- Installing document generators (PDF, PowerPoint)
- And more!

**If you get errors:**

```bash
# Try using pip3 instead
pip3 install -r requirements.txt

# Or with Python directly
python -m pip install -r requirements.txt
```

---

### Step 5: Create Configuration File

We need to tell Nitro AI how to run. Create a file called `.env` in the `backend` folder.

**Windows:**
1. Open Notepad
2. Copy the content below
3. Save as `backend/.env` (make sure it's `.env` not `.env.txt`!)

**Mac/Linux:**
```bash
cd backend
nano .env
# Paste content below, then Ctrl+X, Y, Enter to save
```

**`.env` file content:**

```env
# ============================================
# Nitro AI Configuration - Beginner Setup
# ============================================

# === AI Model Settings ===
AI_MODEL=ollama
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434

# How creative should AI be? (0.0 = boring, 1.0 = very creative)
AI_TEMPERATURE=0.7

# How long can responses be?
AI_MAX_TOKENS=500

# === Server Settings ===
DEBUG_MODE=True
PORT=8000
HOST=0.0.0.0

# === Features (Enable/Disable) ===
ENABLE_VIDEO_GEN=False
ENABLE_WEB_SEARCH=False
ENABLE_TRANSLATION=False
ENABLE_AUTO_LANGUAGE_DETECT=True

# === Language Settings ===
DEFAULT_LANGUAGE=en

# === Optional: Cloud AI APIs ===
# Only needed if you want to use OpenAI instead of Ollama
# OPENAI_API_KEY=sk-your-key-here
```

**💡 Tip:** Leave everything as-is for now. It's perfect for beginners!

---

### Step 6: Start the Backend Server

Open a terminal in the `backend` folder:

```bash
cd backend
python run.py
```

**You should see:**

```
🚀 Nitro AI Backend v4.0 is starting...
📝 Debug mode: True
🌐 Server will run on 0.0.0.0:8000
💾 Memory system initialized
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**🎉 Success!** Your backend is running!

**Keep this terminal window open!** Minimize it, but don't close it.

---

### Step 7: Open the Frontend

**Simple Method:**
1. Navigate to the `frontend` folder
2. Double-click `index.html`
3. It should open in your browser!

**Alternative Method:**
```bash
cd frontend
# Mac/Linux:
open index.html

# Windows:
start index.html
```

**You should see the Nitro AI interface!** 🎊

---

### Step 8: Test Your Setup

1. **Type a message:** "Hello! Can you introduce yourself?"
2. **Press Send** (or hit Enter)
3. **Wait a moment...** The first response might be slow (AI is loading)
4. **See the response!** Your local AI is working!

---

## 🎯 Quick Tests

### Test 1: Basic Chat

**Try asking:**
- "What is Python programming?"
- "Tell me a fun fact"
- "Write me a haiku about coding"

### Test 2: Language Detection

**Try sending:**
- "Bonjour! Comment ça va?" (French)
- "Hola, ¿cómo estás?" (Spanish)
- "こんにちは" (Japanese)

The system should auto-detect the language!

### Test 3: Document Generation

**In Python terminal:**

```bash
# Open a new terminal (keep backend running!)
cd backend
python
```

```python
from document_generator import DocumentGenerator

gen = DocumentGenerator()
gen.generate_pdf(
    title="My First PDF",
    content=["This is a test", "Generated by Nitro AI!"],
    filename="test.pdf"
)
```

**Check `backend/generated_documents/` folder for your PDF!**

---

## 🎨 Customizing Your Setup

### Use a Different AI Model

**Step 1:** Download new model
```bash
ollama pull mistral
```

**Step 2:** Update `.env`
```env
OLLAMA_MODEL=mistral
```

**Step 3:** Restart backend (Ctrl+C, then `python run.py` again)

### Change AI Creativity

More creative (fun, but sometimes random):
```env
AI_TEMPERATURE=0.9
```

More factual (boring but accurate):
```env
AI_TEMPERATURE=0.3
```

### Change Port (if 8000 is taken)

```env
PORT=8001
```

Then open: `http://localhost:8001` instead!

---

## 🐛 Troubleshooting

### Problem: "Cannot connect to Ollama"

**Solution:**
1. Make sure Ollama is installed: `ollama --version`
2. Start Ollama: `ollama serve` (in a new terminal)
3. Verify model is downloaded: `ollama list`

### Problem: "Module not found: aiohttp"

**Solution:**
```bash
pip install aiohttp
```

### Problem: "Address already in use"

**Solution:**
Another program is using port 8000. Change port in `.env`:
```env
PORT=8001
```

### Problem: "Python not found"

**Solution:**
- Windows: Reinstall Python and CHECK "Add to PATH"
- Mac: Use `python3` instead of `python`
- Linux: Install with `sudo apt install python3`

### Problem: Backend starts but frontend can't connect

**Solution:**
1. Check backend is running: `http://localhost:8000/health`
2. Check port in frontend matches backend
3. Try Chrome/Firefox (some browsers block local connections)

### Problem: AI responses are gibberish

**Solution:**
1. Model might be corrupted. Re-download:
   ```bash
   ollama rm llama2
   ollama pull llama2
   ```

### Problem: Very slow responses

**Solution:**
1. Use a smaller model: `ollama pull phi`
2. Reduce max tokens in `.env`: `AI_MAX_TOKENS=200`
3. Close other programs to free RAM

---

## 📚 Next Steps

### 1. Learn the API

Read [PLATFORM_GUIDE.md](PLATFORM_GUIDE.md) for complete API documentation.

### 2. Try Streaming Chat

**In frontend, look for the "Stream" toggle** (if implemented)

Or test with curl:
```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me a story", "user_id": "test"}'
```

### 3. Explore Advanced Features

- **Video Generation:** Coming soon!
- **Web Search:** In development
- **Voice AI:** Planned

### 4. Customize the UI

Edit `frontend/style.css` to change colors, fonts, layout!

### 5. Build Your Own Features

The code is fully open-source and well-commented. Read and modify!

---

## 💡 Tips for Best Experience

### 💰 Save Money
- Use Ollama (100% free, unlimited)
- Only use OpenAI if you need GPT-4 specifically

### ⚡ Speed Tips
- SSD is much faster than HDD for models
- More RAM = better performance
- GPU (optional) makes it MUCH faster

### 🔒 Privacy Tips
- Ollama = 100% private, nothing leaves your computer
- OpenAI = sends data to cloud (but faster/smarter)

### 📊 Quality Tips
- **llama2** = balanced
- **mistral** = better quality
- **llama2:13b** = best quality (needs 8GB RAM)
- **phi** = fastest (but lower quality)

---

## 🎓 Learning Resources

### Python Basics
- [Official Python Tutorial](https://docs.python.org/3/tutorial/)
- [Learn Python in Y Minutes](https://learnxinyminutes.com/docs/python/)

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### Ollama
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Available Models](https://ollama.ai/library)

### AI Prompting
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)

---

## 🎉 Congratulations!

You now have a **fully functional AI platform** running on your computer!

**What you've achieved:**
- ✅ Installed local AI (Ollama)
- ✅ Set up Python backend
- ✅ Configured environment
- ✅ Started web server
- ✅ Tested AI chat
- ✅ Generated documents

**You're ready to:**
- Chat with AI locally (FREE!)
- Generate PDFs and PowerPoints
- Detect languages automatically
- Explore advanced features

---

## 📞 Need Help?

1. **Read documentation:** [PLATFORM_GUIDE.md](PLATFORM_GUIDE.md)
2. **Check troubleshooting** above
3. **Read code comments** (very detailed!)
4. **Open GitHub issue**

---

**🚀 Happy building with Nitro AI!**
