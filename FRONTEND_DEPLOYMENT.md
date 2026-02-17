# 🎨 Nitro AI Frontend Deployment Guide

**Deploy your ChatGPT-style UI to make Nitro AI accessible to users!**

---

## ✅ Prerequisites Completed

- ✅ Backend deployed on Render: https://nitro-ai-pk9l.onrender.com
- ✅ Frontend configured to use production API
- ✅ CORS enabled for cross-origin requests
- ✅ Mobile-responsive PWA ready

---

## 🚀 Quick Deploy Options

### **Option 1: Render (Recommended - Easiest)**

**Why Render?**
- ✅ FREE static site hosting
- ✅ Auto-deploys from GitHub
- ✅ Custom domains (free SSL)
- ✅ CDN included

**Steps:**

1. **Go to Render Dashboard**
   ```
   https://dashboard.render.com/
   ```

2. **Create New Static Site**
   - Click "New +" → "Static Site"
   - Connect your GitHub repository: `NItro-Ai`
   - Click "Connect"

3. **Configure Build Settings**
   - **Name:** `nitro-ai-frontend` (or your choice)
   - **Branch:** `main`
   - **Build Command:** Leave EMPTY (no build needed)
   - **Publish Directory:** `frontend`
   - Click "Create Static Site"

4. **Wait for Deployment**
   - Build completes in ~30 seconds
   - Your frontend will be live at: `https://nitro-ai-frontend.onrender.com`

5. **Update CORS (Important!)**
   - Go to backend service on Render
   - Environment → Edit `ALLOWED_ORIGINS`
   - Add: `https://nitro-ai-frontend.onrender.com`
   - Click "Save Changes" (backend will redeploy)

6. **Test Your App**
   - Visit: `https://nitro-ai-frontend.onrender.com`
   - Start chatting! 🎉

---

### **Option 2: Netlify (Alternative)**

**Why Netlify?**
- ✅ FREE tier generous
- ✅ Instant deployments
- ✅ Drag-and-drop option
- ✅ Great analytics

**Method A: Drag & Drop (Fastest)**

1. **Build Frontend ZIP**
   ```bash
   cd "c:\Nitro AI"
   Compress-Archive -Path frontend\* -DestinationPath nitro-ai-frontend.zip
   ```

2. **Deploy to Netlify**
   - Go to https://app.netlify.com/drop
   - Drag `nitro-ai-frontend.zip` onto the page
   - Wait 10 seconds
   - Your site is live! (e.g., `https://random-name-123.netlify.app`)

3. **Update CORS**
   - Add your Netlify URL to backend `ALLOWED_ORIGINS`

**Method B: GitHub (Auto-Deploy)**

1. **Go to Netlify**
   ```
   https://app.netlify.com/
   ```

2. **Import from Git**
   - Click "Add new site" → "Import an existing project"
   - Choose "GitHub" → Select `NItro-Ai` repo
   - Branch: `main`
   - Build command: Leave empty
   - Publish directory: `frontend`
   - Click "Deploy site"

3. **Configure Domain**
   - Site settings → Domain management
   - Change site name to: `nitro-ai` (if available)
   - Your URL: `https://nitro-ai.netlify.app`

4. **Update CORS**
   - Add Netlify URL to backend environment

---

### **Option 3: Vercel (Developer Favorite)**

**Why Vercel?**
- ✅ Excellent performance
- ✅ Global CDN
- ✅ Instant deployments
- ✅ Preview deployments for PRs

**Steps:**

1. **Install Vercel CLI (Optional)**
   ```bash
   npm install -g vercel
   ```

2. **Deploy via GitHub (Recommended)**
   - Go to https://vercel.com/
   - Click "Add New" → "Project"
   - Import `NItro-Ai` repository
   - Framework: Other
   - Root directory: Leave as `.`
   - Build command: Leave empty
   - Output directory: `frontend`
   - Click "Deploy"

3. **Configure**
   - Vercel auto-detects `vercel.json`
   - Deployment completes in ~20 seconds
   - Your URL: `https://nitro-ai.vercel.app`

4. **Update CORS**
   - Add Vercel URL to backend `ALLOWED_ORIGINS`

**Quick Deploy (CLI):**
```bash
cd "c:\Nitro AI"
vercel --prod
# Follow prompts, select 'frontend' as publish directory
```

---

## 🔧 Post-Deployment Configuration

### 1. **Update Backend CORS**

Go to your Render backend service:

1. Navigate to: https://dashboard.render.com/
2. Select your `nitro-ai` backend service
3. Go to "Environment" tab
4. Find `ALLOWED_ORIGINS` variable
5. Update to include your frontend URL(s):

```
ALLOWED_ORIGINS=https://nitro-ai-frontend.onrender.com,https://nitro-ai.netlify.app,https://nitro-ai.vercel.app
```

6. Click "Save Changes"
7. Backend will auto-redeploy (~2 minutes)

### 2. **Test Full Integration**

Visit your deployed frontend and test:

- [ ] Chat sends message → gets AI response
- [ ] Image generation works (if enabled)
- [ ] Voice features accessible
- [ ] Search functionality works
- [ ] Video generation status updates
- [ ] Mobile responsive layout

### 3. **Custom Domain (Optional)**

**Render:**
- Settings → Custom Domain → Add your domain
- Update DNS records as instructed
- Free SSL certificate auto-provisioned

**Netlify:**
- Domain settings → Add custom domain
- Configure DNS (A record or CNAME)
- SSL automatic

**Vercel:**
- Project Settings → Domains
- Add domain → Follow DNS instructions
- SSL automatic

---

## 📱 Progressive Web App (PWA) Features

Your frontend is already a PWA! Users can:

- **Install on mobile:** "Add to Home Screen"
- **Offline access:** Basic UI works offline
- **App-like experience:** Full-screen, no browser UI

**Files included:**
- ✅ `manifest.json` - App metadata
- ✅ `sw.js` - Service worker for offline
- ✅ Icons and splash screens

---

## 🔒 Security Checklist

- [ ] HTTPS enabled (automatic on all platforms)
- [ ] CORS restricted to your domain (update from `*`)
- [ ] API keys not exposed in frontend
- [ ] Content Security Policy headers set
- [ ] XSS protection enabled

---

## 🎨 Customization

### Update Branding

Edit `frontend/index.html`:
```html
<title>Your Brand - AI Assistant</title>
```

Edit `frontend/manifest.json`:
```json
{
  "name": "Your Brand AI",
  "short_name": "YourAI",
  ...
}
```

### Update Colors

Edit `frontend/style.css`:
```css
:root {
    --primary-color: #your-color;
    --accent-color: #your-accent;
}
```

---

## 📊 Monitoring & Analytics

### Render Analytics
- Dashboard → Analytics tab
- See traffic, bandwidth, requests

### Add Google Analytics (Optional)

Add to `frontend/index.html` before `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
```

---

## 🐛 Troubleshooting

### Issue 1: "Failed to fetch" error

**Cause:** CORS not configured or backend down

**Fix:**
1. Check backend is running: https://nitro-ai-pk9l.onrender.com/health
2. Verify CORS includes your frontend URL
3. Check browser console for exact error

### Issue 2: "Connection refused"

**Cause:** Frontend using wrong API URL

**Fix:**
1. Open browser DevTools → Console
2. Check logged API URL
3. Verify `frontend/config.js` has correct backend URL

### Issue 3: Slow first load

**Cause:** Render free tier - backend sleeps after 15 min idle

**Solutions:**
- Upgrade to paid Render plan ($7/month, no sleep)
- Use UptimeRobot to ping backend every 5 minutes
- Accept 10-30 second cold start delay

### Issue 4: Mobile layout broken

**Cause:** CSS not loading or cache issue

**Fix:**
1. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Clear browser cache
3. Check DevTools → Network tab for failed CSS requests

---

## 🚀 Performance Optimization

### Enable Caching

Already configured in deployment files:
- Static assets: 1 year cache
- HTML/config: No cache (always fresh)

### Compress Assets (Optional)

For even faster loading, compress images:
```bash
# Install tool
npm install -g imagemin-cli

# Compress images (if any in frontend)
imagemin frontend/images/* --out-dir=frontend/images
```

### CDN Benefits

All platforms include free CDN:
- ✅ Fast global delivery
- ✅ DDoS protection
- ✅ Automatic image optimization (some platforms)

---

## 📈 Scaling Options

### Free Tier Limits

**Render Static:**
- ✅ Unlimited bandwidth
- ✅ Unlimited requests
- ✅ 100GB storage

**Netlify:**
- ✅ 100GB bandwidth/month
- ✅ Unlimited sites
- ✅ 300 build minutes/month

**Vercel:**
- ✅ 100GB bandwidth/month
- ✅ Unlimited requests
- ✅ Serverless functions included

### When to Upgrade

Upgrade backend ($7/month) when:
- Users complain about slow cold starts
- Backend needs to be always-on
- Processing heavy workloads

Upgrade frontend (rarely needed) when:
- Exceeding bandwidth limits
- Need advanced features (A/B testing, etc.)

---

## ✅ Deployment Checklist

- [ ] Frontend code pushed to GitHub
- [ ] Static site created on chosen platform
- [ ] Deployment successful (check URL)
- [ ] Backend CORS updated with frontend URL
- [ ] Test chat functionality works end-to-end
- [ ] Mobile responsive verified
- [ ] PWA install tested on mobile
- [ ] Custom domain configured (optional)
- [ ] Analytics added (optional)
- [ ] Share with users! 🎉

---

## 🎯 Quick Deployment Commands

```bash
# Commit frontend changes
cd "c:\Nitro AI"
git add frontend/config.js frontend/index.html frontend/script.js
git add render-static.yaml netlify.toml vercel.json
git commit -m "Configure frontend for production deployment"
git push origin main

# Deploy will happen automatically on:
# - Render (if static site created)
# - Netlify (if connected)
# - Vercel (if connected)
```

---

## 📚 Platform Documentation

- **Render:** https://render.com/docs/static-sites
- **Netlify:** https://docs.netlify.com/
- **Vercel:** https://vercel.com/docs

---

## 🆘 Need Help?

1. **Check backend health:** https://nitro-ai-pk9l.onrender.com/health
2. **Check backend API docs:** https://nitro-ai-pk9l.onrender.com/docs
3. **Browser console:** F12 → Console tab (shows errors)
4. **Platform logs:** Dashboard → Logs (deployment issues)

---

## 🎉 You're Ready!

Your Nitro AI is now accessible as a professional web app!

**Recommended first deployment:** Render (easiest, free, reliable)

**Next steps:**
1. Deploy to Render following steps above
2. Update CORS with frontend URL
3. Test chat functionality
4. Share with friends!

**Your URLs after deployment:**
- Backend API: https://nitro-ai-pk9l.onrender.com
- Frontend UI: https://nitro-ai-frontend.onrender.com (after deployment)

---

*Last Updated: February 17, 2026*
