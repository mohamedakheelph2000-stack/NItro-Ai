# 🌐 Cloudflare Tunnel Setup Guide for Nitro AI

This guide will help you expose your Nitro AI backend (running on `localhost:8000`) to the internet securely using Cloudflare Tunnel.

## 📋 Prerequisites

- ✅ Nitro AI backend running on `localhost:8000`
- ✅ A Cloudflare account (free tier works!)
- ✅ A domain added to Cloudflare (or use a free `.trycloudflare.com` subdomain)
- ✅ Windows PowerShell with admin access

---

## 🚀 Step 1: Install Cloudflared

### Option A: Using Winget (Recommended)
```powershell
# Install cloudflared using Windows Package Manager
winget install --id Cloudflare.cloudflared
```

### Option B: Manual Download
1. Download from: https://github.com/cloudflare/cloudflared/releases/latest
2. Download `cloudflared-windows-amd64.exe`
3. Rename to `cloudflared.exe`
4. Move to `C:\Program Files\cloudflared\`
5. Add to PATH:
   ```powershell
   $env:Path += ";C:\Program Files\cloudflared"
   [System.Environment]::SetEnvironmentVariable("Path", $env:Path, [System.EnvironmentVariableTarget]::Machine)
   ```

### Verify Installation
```powershell
cloudflared --version
# Should show: cloudflared version 2024.x.x
```

---

## 🔐 Step 2: Login to Cloudflare

```powershell
# Navigate to your project
cd "C:\Nitro AI"

# Login to Cloudflare (opens browser)
cloudflared tunnel login
```

**What happens:**
- Browser opens with Cloudflare login
- Select your domain
- Authorization file saved to: `C:\Users\YourName\.cloudflared\cert.pem`

---

## 🏗️ Step 3: Create a Tunnel

```powershell
# Create a named tunnel (replace 'nitro-ai' with your preferred name)
cloudflared tunnel create nitro-ai
```

**Output example:**
```
Tunnel credentials written to C:\Users\YourName\.cloudflared\<TUNNEL-ID>.json
Created tunnel nitro-ai with id <TUNNEL-ID>
```

**Important:** Save your `<TUNNEL-ID>` - you'll need it!

---

## 🗺️ Step 4: Create Tunnel Configuration File

Create a config file at: `C:\Users\YourName\.cloudflared\config.yml`

```yaml
# Cloudflare Tunnel Configuration for Nitro AI
tunnel: <TUNNEL-ID>  # Replace with your tunnel ID from Step 3
credentials-file: C:\Users\YourName\.cloudflared\<TUNNEL-ID>.json

ingress:
  # Route your domain to localhost:8000 (Nitro AI backend)
  - hostname: nitro-ai.yourdomain.com  # Replace with your actual domain
    service: http://localhost:8000
    originRequest:
      noTLSVerify: true
  
  # Catch-all rule (required)
  - service: http_status:404
```

**Configuration breakdown:**
- `tunnel`: Your tunnel ID from Step 3
- `credentials-file`: Path to your tunnel credentials
- `hostname`: Your subdomain (e.g., `nitro-ai.example.com`)
- `service`: Points to your local backend (`http://localhost:8000`)

---

## 🌍 Step 5: Route DNS to Tunnel

```powershell
# Route your domain to the tunnel
cloudflared tunnel route dns nitro-ai nitro-ai.yourdomain.com
```

**What this does:**
- Creates a CNAME record in Cloudflare DNS
- Points `nitro-ai.yourdomain.com` → Your tunnel
- Takes ~1-2 minutes to propagate

**Verify in Cloudflare Dashboard:**
1. Go to your domain's DNS settings
2. You should see a new CNAME record pointing to `<TUNNEL-ID>.cfargotunnel.com`

---

## ▶️ Step 6: Start the Tunnel

### Option A: Run Once (Testing)
```powershell
# Start tunnel in foreground
cloudflared tunnel run nitro-ai
```

**Expected output:**
```
INF Starting tunnel tunnelID=<TUNNEL-ID>
INF Connection registered connector=<ID>
INF Registered tunnel connection
```

Press `Ctrl+C` to stop.

### Option B: Run as Windows Service (Production)

#### Install Service:
```powershell
# Run PowerShell as Administrator
cloudflared service install
```

#### Start Service:
```powershell
# Start the service
Start-Service cloudflared

# Verify it's running
Get-Service cloudflared

# Enable auto-start on boot
Set-Service -Name cloudflared -StartupType Automatic
```

#### Service Management:
```powershell
# Stop service
Stop-Service cloudflared

# Restart service
Restart-Service cloudflared

# Check status
Get-Service cloudflared

# View logs
Get-EventLog -LogName Application -Source cloudflared -Newest 20
```

---

## 🔧 Step 7: Configure Nitro AI for Public Access

### Update Backend Environment Variables

Edit `C:\Nitro AI\backend\.env`:

```env
# ============================================
# PRODUCTION SECURITY SETTINGS
# ============================================

# Your Cloudflare Tunnel domain
CLOUDFLARE_TUNNEL_DOMAIN=https://nitro-ai.yourdomain.com

# Allowed origins for CORS (include your tunnel domain)
ALLOWED_ORIGINS=http://localhost:3000,https://nitro-ai.yourdomain.com

# Enable API key authentication (RECOMMENDED for public access)
ENABLE_API_KEY=True

# Generate a secure API key (run this command):
# python -c "import secrets; print(secrets.token_urlsafe(32))"
API_KEY=your-generated-api-key-here

# Enable rate limiting (RECOMMENDED for production)
ENABLE_RATE_LIMIT=True

# Rate limit: requests per minute per IP
RATE_LIMIT_PER_MINUTE=30
```

### Generate Secure API Key:
```powershell
# Run in your virtual environment
cd "C:\Nitro AI"
.\.venv\Scripts\activate
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and paste into `API_KEY` in your `.env` file.

### Update Frontend Configuration

Edit `C:\Nitro AI\frontend\config.js`:

```javascript
const CONFIG = {
    // Local Backend API URL (for development)
    LOCAL_API_URL: 'http://localhost:8000',
    
    // Cloudflare Tunnel URL (for public access)
    CLOUDFLARE_TUNNEL_URL: 'https://nitro-ai.yourdomain.com',
    
    // API Key (paste the same key from .env)
    API_KEY: 'your-generated-api-key-here',
    
    // ... rest of config
};
```

### Restart Backend
```powershell
# Stop current backend
Get-Process python | Where-Object {$_.Path -like "*uvicorn*"} | Stop-Process

# Start with new config
cd "C:\Nitro AI"
.\.venv\Scripts\activate
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## ✅ Step 8: Test Your Setup

### Test 1: Local Access (Should Still Work)
```powershell
# Test health endpoint locally
Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing
```

### Test 2: Public Access via Tunnel
```powershell
# Test from public domain
Invoke-WebRequest -Uri https://nitro-ai.yourdomain.com/health -UseBasicParsing
```

### Test 3: Frontend Access
1. Open browser: `http://localhost:3000`
2. Should detect Cloudflare Tunnel automatically
3. Send a test message
4. Check browser console for API URL confirmation

### Test 4: Mobile/External Access
1. From your phone/tablet, visit: `https://nitro-ai.yourdomain.com`
2. Should see the Nitro AI interface
3. Chat should work with API key authentication

---

## 🔒 Security Best Practices

### ✅ DO:
- **Enable API Key Authentication** (`ENABLE_API_KEY=True`)
- **Enable Rate Limiting** (`ENABLE_RATE_LIMIT=True`)
- **Use HTTPS only** for public access (Cloudflare provides this automatically)
- **Rotate API keys regularly** (monthly recommended)
- **Monitor logs** for suspicious activity
- **Keep cloudflared updated** (`cloudflared update`)

### ❌ DON'T:
- **Never commit `.env` to Git** (it's already in `.gitignore`)
- **Don't share your API key publicly**
- **Don't disable rate limiting in production**
- **Don't use DEBUG_MODE=True in production**
- **Don't expose Ollama directly** (keep it localhost-only)

---

## 📊 Monitoring & Troubleshooting

### View Tunnel Status
```powershell
# List all tunnels
cloudflared tunnel list

# Show tunnel info
cloudflared tunnel info nitro-ai

# View active connections
Get-Service cloudflared
```

### Common Issues

#### Issue: "Tunnel not connecting"
**Solution:**
```powershell
# Check config file syntax
cloudflared tunnel ingress validate

# Test tunnel manually
cloudflared tunnel --config C:\Users\YourName\.cloudflared\config.yml run nitro-ai
```

#### Issue: "502 Bad Gateway"
**Causes:**
- Backend not running on localhost:8000
- Firewall blocking connections
- Wrong service URL in config.yml

**Solution:**
```powershell
# Verify backend is running
Invoke-WebRequest -Uri http://localhost:8000/health

# Check Windows Firewall
New-NetFirewallRule -DisplayName "Nitro AI Backend" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

#### Issue: "CORS errors in browser"
**Solution:**
- Verify `CLOUDFLARE_TUNNEL_DOMAIN` in `.env` matches your actual domain
- Ensure `ALLOWED_ORIGINS` includes your tunnel domain
- Restart backend after config changes

#### Issue: "401 Unauthorized" errors
**Causes:**
- API key not set in frontend `config.js`
- API key mismatch between backend and frontend
- API key header not being sent

**Solution:**
- Verify `API_KEY` matches in both `.env` and `config.js`
- Check browser console for API key in request headers
- Test with: `Invoke-WebRequest -Uri https://nitro-ai.yourdomain.com/health -Headers @{"X-API-Key"="your-key"}`

#### Issue: "429 Too Many Requests"
**Causes:**
- Rate limit exceeded (30 requests/minute by default)

**Solution:**
- Increase `RATE_LIMIT_PER_MINUTE` in `.env`
- Wait 60 seconds and try again
- Check for loops/automated scripts causing excess requests

---

## 🎯 Quick Reference Commands

```powershell
# === TUNNEL MANAGEMENT ===

# Start tunnel (foreground)
cloudflared tunnel run nitro-ai

# Install as service
cloudflared service install

# Start/Stop service
Start-Service cloudflared
Stop-Service cloudflared

# View tunnel status
cloudflared tunnel list
cloudflared tunnel info nitro-ai

# Update cloudflared
cloudflared update

# === BACKEND MANAGEMENT ===

# Generate new API key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Restart backend
cd "C:\Nitro AI\backend"
.\.venv\Scripts\activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Test backend health
Invoke-WebRequest -Uri http://localhost:8000/health
Invoke-WebRequest -Uri https://nitro-ai.yourdomain.com/health

# === LOGS & DEBUGGING ===

# View cloudflared logs
Get-EventLog -LogName Application -Source cloudflared -Newest 20

# View backend logs
cd "C:\Nitro AI\backend"
Get-Content server.log -Tail 50

# Test with verbose output
cloudflared tunnel --loglevel debug run nitro-ai
```

---

## 🌟 Advanced Configuration

### Multiple Backends (Frontend + Backend)

If you want to serve both frontend and backend through the tunnel:

```yaml
# config.yml
tunnel: <TUNNEL-ID>
credentials-file: C:\Users\YourName\.cloudflared\<TUNNEL-ID>.json

ingress:
  # Frontend (static files)
  - hostname: nitro-ai.yourdomain.com
    service: http://localhost:3000
  
  # Backend API
  - hostname: api.nitro-ai.yourdomain.com
    service: http://localhost:8000
    originRequest:
      noTLSVerify: true
  
  # Catch-all
  - service: http_status:404
```

Then route both domains:
```powershell
cloudflared tunnel route dns nitro-ai nitro-ai.yourdomain.com
cloudflared tunnel route dns nitro-ai api.nitro-ai.yourdomain.com
```

Update frontend `config.js`:
```javascript
CLOUDFLARE_TUNNEL_URL: 'https://api.nitro-ai.yourdomain.com',
```

### IP Whitelisting (Extra Security)

Add to Cloudflare dashboard → Security → WAF:
1. Create firewall rule
2. Field: `IP Address`
3. Operator: `is not in`
4. Value: Your trusted IPs
5. Action: `Block`

---

## 📱 Using from Mobile/External Devices

Once your tunnel is running:

1. **From any device with internet:**
   - Navigate to `https://nitro-ai.yourdomain.com`
   - Interface loads from tunnel
   - Chat works with API key authentication

2. **Security Notice:**
   - All traffic encrypted via Cloudflare's HTTPS
   - Your laptop must be on and running the backend
   - Ollama must be active for AI responses

3. **Performance:**
   - Latency: +50-200ms (depends on Cloudflare edge location)
   - Bandwidth: Minimal (text-only chat)
   - Your laptop's internet upload speed matters

---

## 🔄 Keeping Tunnel Running 24/7

### Option 1: Windows Service (Recommended)
Already covered in Step 6 - automatically restarts on boot.

### Option 2: Task Scheduler
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "cloudflared.exe" -Argument "tunnel run nitro-ai"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "Cloudflare Tunnel - Nitro AI" -Action $action -Trigger $trigger -Principal $principal
```

### Option 3: PM2 (Alternative)
```powershell
# Install PM2
npm install -g pm2

# Start tunnel with PM2
pm2 start cloudflared --name nitro-ai -- tunnel run nitro-ai

# Save PM2 config
pm2 save

# Enable PM2 startup
pm2 startup
```

---

## 📞 Support & Resources

- **Cloudflare Tunnel Docs:** https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- **Nitro AI Issues:** `C:\Nitro AI\TROUBLESHOOTING.md`
- **Cloudflare Community:** https://community.cloudflare.com/

---

## ✨ Summary Checklist

- [ ] Cloudflared installed and verified
- [ ] Logged into Cloudflare account
- [ ] Tunnel created with unique name
- [ ] Config.yml created with correct tunnel ID
- [ ] DNS routed to tunnel
- [ ] Backend .env configured with tunnel domain
- [ ] API key generated and set
- [ ] Rate limiting enabled
- [ ] Frontend config.js updated with tunnel URL
- [ ] Backend restarted with new config
- [ ] Tunnel running (service or foreground)
- [ ] Local access tested (localhost:8000)
- [ ] Public access tested (your domain)
- [ ] Mobile access tested
- [ ] Security headers verified
- [ ] CORS working correctly

**You're ready!** Your Nitro AI is now accessible from anywhere on the internet, securely protected by Cloudflare Tunnel. 🚀

---

**Last Updated:** February 19, 2026  
**Version:** 6.0 - Public Access Ready
