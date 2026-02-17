# Nitro AI Backend

A lightweight FastAPI backend server for the Nitro AI assistant platform.

## 🚀 Getting Started (Step-by-Step for Beginners)

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed on your computer.

**Check if Python is installed:**
```bash
python --version
```

If you don't have Python, download it from [python.org](https://www.python.org/downloads/)

---

### Step 2: Create a Virtual Environment (Recommended)

A virtual environment keeps your project dependencies separate from other Python projects.

**On Windows:**
```bash
cd "c:\Nitro AI\backend"
python -m venv venv
venv\Scripts\activate
```

**On Linux/macOS:**
```bash
cd "/c/Nitro AI/backend"
python3 -m venv venv
source venv/bin/activate
```

You'll see `(venv)` appear in your terminal when it's activated. This means you're inside the virtual environment.

---

### Step 3: Install Dependencies

Now install all the required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

This will install:
- **FastAPI** - Our web framework
- **Uvicorn** - The server that runs our app
- **Pydantic** - Data validation
- **Python-multipart** - For handling forms

**Wait for installation to complete.** You'll see packages being downloaded and installed.

---

### Step 4: Run the Backend Server

Start the server with this command:

```bash
uvicorn main:app --reload
```

**What does this mean?**
- `uvicorn` - The server program
- `main:app` - Run the `app` from `main.py` file
- `--reload` - Automatically restart when you change code (great for development!)

---

### Step 5: Test Your Server

Once running, you'll see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Test these URLs in your browser:**

1. **Root endpoint:** http://localhost:8000/
   - Should show: "Welcome to Nitro AI Backend!"

2. **Health check:** http://localhost:8000/health
   - Should show server status and timestamp

3. **API Documentation (Auto-generated!):** http://localhost:8000/docs
   - This is AMAZING! FastAPI automatically creates interactive documentation
   - You can test the `/chat` endpoint right here in your browser!

---

### Step 6: Test the Chat Endpoint

**Option A: Use the Interactive Docs (Easiest)**
1. Go to http://localhost:8000/docs
2. Click on `POST /chat`
3. Click "Try it out"
4. Enter this JSON in the request body:
   ```json
   {
     "message": "Hello Nitro AI!",
     "user_id": "beginner_user"
   }
   ```
5. Click "Execute"
6. See the response below!

**Option B: Use PowerShell (Windows)**
```powershell
$body = @{
    message = "Hello Nitro AI!"
    user_id = "test_user"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/chat -Method Post -Body $body -ContentType "application/json"
```

**Option C: Use curl (Linux/macOS or Windows with curl installed)**
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello Nitro AI!", "user_id": "test_user"}'
```

---

## 📁 File Structure

```
backend/
├── main.py              # Main server file with all endpoints
├── requirements.txt     # List of dependencies to install
└── README.md           # This file (instructions)
```

---

## 🎯 What We Built

1. **A FastAPI server** - Lightweight and fast web framework
2. **Three endpoints:**
   - `GET /` - Welcome message
   - `GET /health` - Health check
   - `POST /chat` - Main chat endpoint (currently returns dummy responses)
3. **CORS enabled** - So your frontend can communicate with the backend
4. **Clean, well-commented code** - Easy to understand and modify

---

## 🔄 Next Steps

1. ✅ You've created a working backend!
2. 🎨 Next: Build a frontend to interact with this backend
3. 🤖 Later: Connect an AI model to generate intelligent responses
4. 💾 Eventually: Add the memory system to remember conversations

---

## 🛑 How to Stop the Server

Press `Ctrl + C` in the terminal where the server is running.

---

## 💡 Tips for Beginners

- **Keep the terminal open** while the server is running
- **Check the terminal** for error messages if something goes wrong
- **The server restarts automatically** when you save changes to `main.py` (thanks to `--reload`)
- **Visit `/docs`** anytime to see and test all your endpoints
- **Don't worry if you make mistakes** - that's how we learn! Just check the error messages and fix them.

---

## 🆘 Troubleshooting

**Problem: "python: command not found"**
- Solution: Install Python from python.org or use `python3` instead of `python`

**Problem: "Port 8000 is already in use"**
- Solution: Either stop the other program using port 8000, or run on a different port:
  ```bash
  uvicorn main:app --reload --port 8001
  ```

**Problem: "Module not found"**
- Solution: Make sure your virtual environment is activated and you ran `pip install -r requirements.txt`

---

**Happy coding! You're on your way to building your own AI assistant! 🚀**
