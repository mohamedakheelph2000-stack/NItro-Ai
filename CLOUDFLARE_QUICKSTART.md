# 🚀 Cloudflare Tunnel - Quick Start

**Expose your Nitro AI backend to the internet in 5 minutes!**

## 🎯 Quick Steps

### 1. Run Setup Script (Automated)
```powershell
# Run PowerShell as Administrator
cd "C:\Nitro AI"
.\setup-cloudflare-tunnel.ps1
```

The script will:
- ✅ Install cloudflared (if needed)
- ✅ Login to Cloudflare
- ✅ Create tunnel
- ✅ Configure DNS
- ✅ Generate API key
- ✅ Create config file

### 2. Update Configuration Files

**Backend (.env):**
```env
CLOUDFLARE_TUNNEL_DOMAIN=https://your-domain.com
ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com
ENABLE_API_KEY=True
API_KEY=your-generated-key
ENABLE_RATE_LIMIT=True
```

**Frontend (config.js):**
```javascript
CLOUDFLARE_TUNNEL_URL: 'https://your-domain.com',
API_KEY: 'your-generated-key',
```

### 3. Start Tunnel

**Option A: Foreground (Testing)**
```powershell
cloudflared tunnel run nitro-ai
```

**Option B: Windows Service (Production)**
```powershell
cloudflared service install
Start-Service cloudflared
```

### 4. Test Access

```powershell
# Test locally
Invoke-WebRequest http://localhost:8000/health

# Test publicly
Invoke-WebRequest https://your-domain.com/health
```

## 📚 Full Documentation

- **Complete Guide:** [CLOUDFLARE_TUNNEL_GUIDE.md](CLOUDFLARE_TUNNEL_GUIDE.md)
- **Troubleshooting:** See guide Section 9
- **Security Best Practices:** See guide Section 8

## 🔑 Manual Setup (Alternative)

If you prefer manual setup:

```powershell
# 1. Install cloudflared
winget install Cloudflare.cloudflared

# 2. Login
cloudflared tunnel login

# 3. Create tunnel
cloudflared tunnel create nitro-ai

# 4. Route DNS
cloudflared tunnel route dns nitro-ai your-domain.com

# 5. Run tunnel
cloudflared tunnel run nitro-ai
```

## ⚠️ Security Checklist

Before going public:
- [ ] API key enabled (`ENABLE_API_KEY=True`)
- [ ] Rate limiting enabled (`ENABLE_RATE_LIMIT=True`)
- [ ] Strong API key generated (32+ characters)
- [ ] Debug mode disabled (`DEBUG_MODE=False`)
- [ ] CORS configured with specific domains (not `*`)
- [ ] .env file NOT committed to Git

## 🆘 Common Issues

**"Tunnel not connecting"**
→ Check backend is running on localhost:8000

**"502 Bad Gateway"**
→ Verify config.yml service URL is correct

**"CORS errors"**
→ Add your domain to ALLOWED_ORIGINS in .env

**"401 Unauthorized"**
→ Ensure API_KEY matches in .env and config.js

## 📞 Need Help?

See [CLOUDFLARE_TUNNEL_GUIDE.md](CLOUDFLARE_TUNNEL_GUIDE.md) for detailed troubleshooting.

---

**Made with ❤️ for Nitro AI**  
*Secure, fast, and always accessible!*
