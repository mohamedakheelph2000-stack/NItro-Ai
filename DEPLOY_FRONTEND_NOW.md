# 🚀 Deploy Nitro AI Frontend to Netlify (5 Minutes)

## ✅ Status Check

- ✅ Backend deployed: https://nitro-ai-pk9l.onrender.com
- ✅ Frontend configured for production
- ✅ CORS ready (needs URL update after deploy)
- ✅ Responsive PWA ready

---

## 🎯 Deploy to Netlify (Recommended)

### Method 1: Drag & Drop (Fastest - 2 Minutes)

1. **Create Frontend ZIP**
   ```powershell
   cd "c:\Nitro AI"
   Compress-Archive -Path frontend\* -DestinationPath nitro-ai-frontend.zip -Force
   ```

2. **Deploy**
   - Go to: https://app.netlify.com/drop
   - Drag `nitro-ai-frontend.zip` onto the page
   - Wait 10 seconds ⏱️
   - **Your site is LIVE!** 🎉

3. **Get Your URL**
   - Example: `https://dreamy-cupcake-a1b2c3.netlify.app`
   - Copy this URL

4. **Update Backend CORS**
   - Go to: https://dashboard.render.com/
   - Select your backend service: `nitro-ai-pk9l`
   - Environment tab → Find `ALLOWED_ORIGINS`
   - Change from `*` to your Netlify URL:
     ```
     https://your-site-name.netlify.app
     ```
   - Click "Save Changes"
   - Backend redeploys (~2 min)

5. **Test**
   - Visit your Netlify URL
   - Start chatting! 💬

---

### Method 2: GitHub Auto-Deploy (Professional)

1. **Connect Netlify to GitHub**
   - Go to: https://app.netlify.com/
   - Click "Add new site" → "Import an existing project"
   - Choose "Deploy with GitHub"
   - Authorize Netlify
   - Select repository: `NItro-Ai`

2. **Configure Build**
   - Branch: `main`
   - Build command: *Leave empty*
   - Publish directory: `frontend`
   - Click "Deploy site"

3. **Customize Site Name**
   - Site settings → Site details
   - Change site name to: `nitro-ai` (or your choice)
   - New URL: `https://nitro-ai.netlify.app`

4. **Update Backend CORS**
   - Same as Method 1, step 4

5. **Auto-Deploy Enabled**
   - Every git push auto-deploys
   - See previews for pull requests

---

## 🔧 Post-Deployment Setup

### 1. Update CORS (Critical!)

**On Render Backend:**
```bash
# Environment variable on Render
ALLOWED_ORIGINS=https://your-netlify-site.netlify.app

# For multiple domains (frontend + custom domain):
ALLOWED_ORIGINS=https://nitro-ai.netlify.app,https://yourdomain.com
```

### 2. Test Full Integration

Visit your Netlify URL and verify:
- [ ] Chat interface loads
- [ ] Send a message → Get AI response
- [ ] No CORS errors in browser console (F12)
- [ ] Mobile responsive (test on phone)
- [ ] PWA install prompt appears

### 3. Custom Domain (Optional)

**In Netlify:**
1. Domain settings → Add custom domain
2. Enter your domain: `yourdomain.com`
3. Update DNS records:
   ```
   Type: CNAME
   Name: www
   Value: your-site-name.netlify.app
   ```
4. SSL auto-provisions (5-10 min)

**Update CORS with new domain!**

---

## 📱 Mobile PWA Installation

Users can install your app:

**On iOS:**
1. Open in Safari
2. Tap Share button
3. "Add to Home Screen"

**On Android:**
1. Open in Chrome
2. Tap menu (3 dots)
3. "Install app"

---

## 🎨 Customization

### Change Site Name

**Netlify:**
- Site settings → Site details → Change site name
- Get a better URL: `nitro-ai.netlify.app`

### Update Branding

**Edit `frontend/index.html`:**
```html
<title>Your Brand - AI Assistant</title>
```

**Edit `frontend/manifest.json`:**
```json
{
  "name": "Your Brand AI",
  "short_name": "YourAI"
}
```

**Commit and push:**
```bash
git add frontend/
git commit -m "Update branding"
git push origin main
# Netlify auto-deploys in 30 seconds
```

---

## 🐛 Troubleshooting

### ❌ "Failed to fetch" Error

**Cause:** CORS not configured

**Fix:**
1. Check backend CORS includes frontend URL
2. Verify backend is running: https://nitro-ai-pk9l.onrender.com/health
3. Clear browser cache (Ctrl+Shift+Delete)

### ❌ Deployment Failed

**Netlify shows error:**
- Check publish directory is `frontend`
- Ensure `netlify.toml` exists in repo root
- Verify all files committed to GitHub

### ❌ Slow First Response

**Cause:** Render free tier - backend sleeps after 15 min

**Solutions:**
1. Wait 10-30 seconds for cold start
2. Upgrade backend to paid ($7/month - no sleep)
3. Use UptimeRobot to ping backend every 5 min

### ❌ Mobile UI Broken

**Fix:**
1. Hard refresh: Pull down on mobile
2. Clear app cache
3. Reinstall PWA

---

## 📊 Monitor Performance

### Netlify Analytics

1. Site dashboard → Analytics
2. See visitors, bandwidth, page views

### Add Google Analytics (Optional)

Add to `frontend/index.html` before `</head>`:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🚀 Alternative: Vercel Deployment

**If you prefer Vercel:**

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd "c:\Nitro AI"
vercel --prod

# Follow prompts:
# - Root: .
# - Output: frontend
```

Your app deploys to: `https://nitro-ai.vercel.app`

---

## ✅ Final Checklist

- [ ] Frontend deployed to Netlify
- [ ] Custom site name configured
- [ ] Backend CORS updated with frontend URL
- [ ] Chat tested end-to-end
- [ ] Mobile responsive verified
- [ ] PWA install tested
- [ ] Analytics added (optional)
- [ ] Custom domain configured (optional)
- [ ] Share with users! 🎉

---

## 🎯 Quick Commands

```powershell
# Create deployment package
cd "c:\Nitro AI"
Compress-Archive -Path frontend\* -DestinationPath nitro-ai-frontend.zip -Force

# Or deploy via GitHub (already pushed)
git status
# Should show: "Your branch is up to date with 'origin/main'"
# Netlify will auto-deploy from GitHub
```

---

## 📞 Support Links

- **Backend Health:** https://nitro-ai-pk9l.onrender.com/health
- **Backend API Docs:** https://nitro-ai-pk9l.onrender.com/docs
- **Netlify Dashboard:** https://app.netlify.com/
- **Render Dashboard:** https://dashboard.render.com/

---

## 🎉 Success!

Your Nitro AI is now:
- ✅ Accessible worldwide
- ✅ ChatGPT-style interface
- ✅ Mobile responsive PWA
- ✅ Auto-deploying on updates
- ✅ Free hosting (Netlify + Render)

**Your URLs:**
- Frontend: `https://your-site.netlify.app`
- Backend: `https://nitro-ai-pk9l.onrender.com`

**Time to deploy:** 5 minutes
**Cost:** $0 (free tier)

---

*Deployed: February 17, 2026*
