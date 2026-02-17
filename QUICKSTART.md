# 🎯 Nitro AI - Quick Start Guide

This guide will get you up and running in 5 minutes!

---

## 🚀 Super Quick Start

### 1. Start Backend (Terminal 1)

```powershell
cd "c:\Nitro AI\backend"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Wait for**: "Uvicorn running on http://127.0.0.1:8000"

### 2. Open Frontend (Browser)

1. Open File Explorer
2. Navigate to `c:\Nitro AI\frontend`
3. Double-click `index.html`

**Done!** 🎉 Start chatting!

---

## ✅ Verify Everything Works

1. **Backend running?** 
   - See "Uvicorn running..." in terminal ✓

2. **Frontend loaded?**
   - See purple Nitro AI interface ✓

3. **Connected?**
   - Green "Connected" indicator in top-right ✓

4. **Can chat?**
   - Type "Hello!" and press Enter ✓
   - See AI response (dummy for now) ✓

5. **History works?**
   - See sidebar on left with sessions ✓
   - Click "New Chat" works ✓

---

## 🎯 Key Features to Try

### 1. Send Messages
- Type in the input box
- Press Enter (or click send button)
- See your message on right (purple)
- See AI response on left (white)

### 2. Chat History
- Look at left sidebar
- See all your conversations
- Click any session to load it

### 3. New Conversation
- Click "New Chat" button
- Previous chat is saved automatically
- Start fresh

### 4. Statistics
- Bottom of sidebar shows:
  - Total sessions
  - Total messages

---

## 🐛 Troubleshooting

### Problem: "Command not found: python"
**Fix**: Try `python3` instead of `python`

### Problem: "Port 8000 already in use"
**Fix**: 
```powershell
# Stop other program using port 8000, or:
uvicorn main:app --reload --port 8001
# Then update frontend/script.js line 7 to use port 8001
```

### Problem: Frontend shows "Disconnected"
**Fix**:
1. Make sure backend is running
2. Check terminal for errors
3. Refresh browser page

### Problem: "Module not found"
**Fix**:
```powershell
# Make sure virtual environment is activated
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📖 Next Steps

Now that it's working:

1. **Explore the Interface**
   - Try different messages
   - Load old conversations
   - Start multiple chats

2. **Check the Code**
   - Look at `backend/main.py` - See how API works
   - Look at `frontend/script.js` - See how frontend works
   - Everything is commented for learning!

3. **Add Real AI** (Optional)
   - See [AI Integration Guide](models/ai_modules/README.md)
   - Start with free Ollama for local AI
   - Or use OpenAI API

4. **Customize**
   - Change colors in `frontend/style.css`
   - Modify responses in `backend/main.py`
   - Add your own features!

---

## 💡 Understanding the Flow

```
User types message
    ↓
frontend/script.js captures it
    ↓
Sends POST to http://localhost:8000/chat
    ↓
backend/main.py receives it
    ↓
Saves to memory/conversations.json
    ↓
Generates response (dummy for now)
    ↓
Sends back to frontend
    ↓
frontend displays AI response
    ↓
Done! ✨
```

---

## 🎨 Quick Customizations

### Change Theme Color
Edit `frontend/style.css` line 16:
```css
/* Current: Purple */
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Try: Blue */
--primary-gradient: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);

/* Try: Green */
--primary-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
```

### Change Welcome Message
Edit `frontend/index.html` line ~62 (welcome message text)

### Change AI Response
Edit `backend/main.py` line ~145 (dummy_response variable)

---

## 📞 Need More Help?

- **Full Documentation**: See main [README.md](README.md)
- **Backend Details**: See [backend/README.md](backend/README.md)
- **Frontend Details**: See [frontend/README.md](frontend/README.md)
- **AI Integration**: See [models/ai_modules/README.md](models/ai_modules/README.md)

---

## ✨ You're All Set!

Your Nitro AI is ready to use!

**Enjoy building your AI assistant!** 🚀

---

*If something doesn't work, check the detailed guides above or review the terminal output for error messages.*
