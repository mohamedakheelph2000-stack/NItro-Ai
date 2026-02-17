# 🚀 NITRO AI BACKEND - SETUP & TESTING GUIDE
# Complete beginner-friendly guide to get your backend running

## ✅ STEP 1: VERIFY YOUR SETUP

You should have these files in your backend folder:
- main.py (main server file)
- config.py (configuration settings)
- schemas.py (data models)
- logger.py (logging system)
- requirements.txt (dependencies list)
- .env.example (environment template)
- .gitignore (git ignore file)
- README.md (this file)

To check, run this in PowerShell:
```powershell
cd "c:\Nitro AI\backend"
dir
```

You should see all 8 files listed above. ✓

---

## 🐍 STEP 2: CHECK PYTHON VERSION

Make sure Python is installed and is version 3.8 or higher.

```powershell
python --version
```

Expected output: `Python 3.8.x` or higher

**If Python is not installed:**
1. Download from: https://www.python.org/downloads/
2. During installation, CHECK "Add Python to PATH"
3. Restart PowerShell after installation

---

## 📦 STEP 3: CREATE VIRTUAL ENVIRONMENT

**What is a virtual environment?**
Think of it as a separate room for your project. It keeps your Nitro AI dependencies separate from other Python projects on your computer.

### Create the virtual environment:
```powershell
cd "c:\Nitro AI\backend"
python -m venv venv
```

This creates a `venv` folder. It might take 30-60 seconds.

### Activate the virtual environment:
```powershell
venv\Scripts\activate
```

**Success indicator:** You'll see `(venv)` at the start of your command line:
```
(venv) PS c:\Nitro AI\backend>
```

**Important:** You need to activate the virtual environment every time you open a new terminal!

---

## 📥 STEP 4: INSTALL DEPENDENCIES

Now install all required packages:

```powershell
pip install -r requirements.txt
```

**What gets installed?**
- FastAPI (web framework) - ~5 MB
- Uvicorn (web server) - ~3 MB
- Pydantic (data validation) - ~2 MB
- Python-dotenv (environment variables) - ~20 KB
- Python-multipart (file uploads) - ~30 KB

**Total: ~10-15 MB** (lightweight for your laptop!)

**Expected output:** You'll see packages being downloaded and installed. Wait until you see "Successfully installed..."

**Verify installation:**
```powershell
pip list
```

You should see all the packages listed.

---

## 🎬 STEP 5: RUN THE BACKEND SERVER

Now for the exciting part - start your server!

```powershell
uvicorn main:app --reload
```

**What does this command mean?**
- `uvicorn` = The web server program
- `main:app` = Run the `app` from `main.py` file
- `--reload` = Auto-restart when you change code (super useful!)

**Expected output:**
```
[2026-02-17 10:30:00] INFO - 🚀 Nitro AI Backend v1.0.0 is starting...
[2026-02-17 10:30:00] INFO - 📝 Debug mode: True
[2026-02-17 10:30:00] INFO - 🌐 Server will run on 0.0.0.0:8000
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**🎉 SUCCESS!** Your server is running!

**To stop the server:** Press `Ctrl + C`

---

## 🧪 STEP 6: TEST YOUR API

### Method 1: Browser (Easiest!) 🌐

Open your browser and visit these URLs:

#### Test 1: Root Endpoint
**URL:** http://localhost:8000/

**Expected Response:**
```json
{
  "message": "Welcome to Nitro AI Backend!",
  "status": "running",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

✅ If you see this, your server is working!

#### Test 2: Health Check
**URL:** http://localhost:8000/health

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-17T10:30:00.123456",
  "version": "1.0.0"
}
```

✅ This confirms the server is healthy!

#### Test 3: Interactive API Documentation (AMAZING!)
**URL:** http://localhost:8000/docs

This opens **Swagger UI** - a beautiful interactive interface where you can:
- See all your API endpoints
- Test them directly in the browser
- See request/response examples
- No additional tools needed!

**Try testing the /chat endpoint:**
1. Click on "POST /chat"
2. Click "Try it out"
3. Replace the example with:
```json
{
  "message": "Hello Nitro AI!",
  "user_id": "tester"
}
```
4. Click "Execute"
5. Scroll down to see the response!

---

### Method 2: PowerShell (For Advanced Testing) 💻

Test the GET endpoint:
```powershell
Invoke-RestMethod -Uri http://localhost:8000/ -Method Get
```

Test the POST /chat endpoint:
```powershell
$body = @{
    message = "Hello Nitro AI!"
    user_id = "tester"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/chat -Method Post -Body $body -ContentType "application/json"
```

---

### Method 3: Postman (Optional) 📮

If you have Postman installed:

**Test GET /**
1. Create new request
2. Method: GET
3. URL: http://localhost:8000/
4. Click "Send"

**Test POST /chat**
1. Create new request
2. Method: POST
3. URL: http://localhost:8000/chat
4. Body tab → Raw → JSON
5. Enter:
```json
{
  "message": "Hello Nitro AI!",
  "user_id": "tester"
}
```
6. Click "Send"

---

## 📊 UNDERSTANDING THE LOGS

When you test your API, watch the terminal where the server is running. You'll see logs like:

```
[2026-02-17 10:35:22] INFO - Root endpoint accessed
INFO:     127.0.0.1:52143 - "GET / HTTP/1.1" 200 OK
[2026-02-17 10:36:15] INFO - Received message from tester: Hello Nitro AI!...
[2026-02-17 10:36:15] INFO - Sending response to tester
INFO:     127.0.0.1:52143 - "POST /chat HTTP/1.1" 200 OK
```

**What do these mean?**
- First line: Our custom log from logger.py
- Second line: Uvicorn's access log
- `200 OK` means the request was successful!

---

## 🎯 AVAILABLE ENDPOINTS

| Endpoint | Method | Description | Test in Browser? |
|----------|--------|-------------|------------------|
| `/` | GET | Welcome message | ✅ Yes |
| `/health` | GET | Health check | ✅ Yes |
| `/chat` | POST | Send chat message | ❌ Use /docs |
| `/docs` | GET | API documentation | ✅ Yes |

---

## ✅ VERIFICATION CHECKLIST

Go through this checklist to confirm everything works:

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Virtual environment created (`venv` folder exists)
- [ ] Virtual environment activated (`(venv)` in terminal)
- [ ] Dependencies installed (`pip list` shows packages)
- [ ] Server starts without errors (`uvicorn main:app --reload`)
- [ ] http://localhost:8000/ shows welcome message
- [ ] http://localhost:8000/health shows healthy status
- [ ] http://localhost:8000/docs shows interactive documentation
- [ ] Can test /chat endpoint in /docs interface
- [ ] Logs appear in terminal when testing endpoints

---

## 🎓 BEGINNER TIPS

### What is localhost?
- `localhost` or `127.0.0.1` = your own computer
- Port `8000` = a door number where your server listens
- Like having a web server running only on your laptop

### What is an endpoint?
- A URL path that does something specific
- Like different pages on a website
- `/chat` is for chatting, `/health` is for checking health

### What is JSON?
- A format to send/receive data
- Easy for both humans and computers to read
- Used by almost all modern APIs

### Understanding HTTP methods:
- **GET** = "Give me information" (like reading)
- **POST** = "Here's some data" (like submitting a form)
- **200 OK** = Success!
- **400 Bad Request** = Your data is wrong
- **500 Internal Server Error** = Server has a problem

---

## 🐛 TROUBLESHOOTING

### Problem: "python: command not found"
**Solution:** Install Python from python.org OR use `python3` instead of `python`

### Problem: "uvicorn: command not found"
**Solution:** 
1. Make sure virtual environment is activated (`(venv)` visible)
2. Run `pip install -r requirements.txt` again

### Problem: "Port 8000 is already in use"
**Solution:** 
- Stop the other server using port 8000
- OR use a different port: `uvicorn main:app --reload --port 8001`

### Problem: "Module not found: config"
**Solution:**
- Make sure you're in the `backend` folder: `cd "c:\Nitro AI\backend"`
- All Python files (main.py, config.py, etc.) must be in the same folder

### Problem: Can't access http://localhost:8000/
**Solution:**
- Check that the server is actually running (no errors in terminal)
- Try http://127.0.0.1:8000/ instead
- Check firewall isn't blocking port 8000

### Problem: Changes to code don't apply
**Solution:**
- Make sure you used `--reload` flag
- If not, stop server (Ctrl+C) and restart it
- Save your file before testing!

---

## 🚀 PERFORMANCE OPTIMIZATION (For Low-Compute Laptops)

Your backend is already optimized for low-power machines:

✅ **Lightweight packages** - Only ~15 MB total
✅ **No AI model loaded yet** - Keeps memory low
✅ **Async FastAPI** - Efficient request handling
✅ **Minimal logging** - Not writing huge log files
✅ **No database yet** - Reduces resource usage

**Current resource usage:**
- RAM: ~50-100 MB
- CPU: ~1-2% when idle
- Disk: ~15 MB

This will run smoothly even on older laptops!

---

## 📝 NEXT STEPS

Now that your backend is working:

1. ✅ **Backend is running!** (You are here)
2. 🎨 Next: Create a simple frontend (HTML/JavaScript)
3. 🔗 Then: Connect frontend to backend
4. 🤖 Later: Add AI model integration
5. 💾 Eventually: Add database for conversation history

---

## 🎉 CONGRATULATIONS!

You've successfully:
- ✅ Set up a professional FastAPI backend
- ✅ Installed all dependencies
- ✅ Run the server locally
- ✅ Tested all endpoints
- ✅ Understood the basics of APIs

**You're ready to build amazing things with Nitro AI! 🚀**

---

## 📞 QUICK REFERENCE COMMANDS

```powershell
# Navigate to backend
cd "c:\Nitro AI\backend"

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload

# Stop server
Press Ctrl + C

# Deactivate virtual environment
deactivate
```

---

**Remember:** Keep the terminal open while the server is running. Open a new terminal window if you need to run other commands!

**Happy coding! 🎊**
