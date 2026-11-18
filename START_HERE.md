# 🚀 START HERE - Deployment Guide

Welcome! Your app is configured for deployment. Choose your path below.

---

## ⚡ Option 1: Fast Deploy (15 minutes)

**For people who just want to get live!**

1. Open: `QUICKSTART_DEPLOY.md`
2. Follow 5 steps
3. Done! Your app is live

**Time:** ~15 minutes  
**Effort:** Low  
**Documentation:** Minimal  

➡️ **Read:** `QUICKSTART_DEPLOY.md`

---

## 📖 Option 2: Full Deploy (30 minutes)

**For people who want to understand everything!**

1. Open: `DEPLOYMENT.md`
2. Follow detailed steps with explanations
3. Reference: `ENV_SETUP.md` for environment variables
4. Use: `DEPLOYMENT_CHECKLIST.md` for testing

**Time:** ~30 minutes  
**Effort:** Medium  
**Documentation:** Comprehensive  

➡️ **Read:** `DEPLOYMENT.md`

---

## ✅ Option 3: By-The-Book Deploy (1 hour)

**For people who want complete control and understanding!**

1. Read: `DEPLOYMENT_COMPLETE.md` (overview)
2. Read: `ENV_SETUP.md` (environment setup)
3. Read: `DEPLOYMENT.md` (step-by-step)
4. Use: `DEPLOYMENT_CHECKLIST.md` (testing)
5. Execute each step carefully

**Time:** ~1 hour  
**Effort:** High  
**Documentation:** Maximum  

➡️ **Read:** `DEPLOYMENT_COMPLETE.md` first

---

## 📁 What's Available

### Quick Reference
- `QUICKSTART_DEPLOY.md` - 15-min fast track ⚡
- `DEPLOYMENT_COMPLETE.md` - Setup overview ℹ️

### Detailed Guides
- `DEPLOYMENT.md` - Full step-by-step guide 📖
- `ENV_SETUP.md` - Environment variables explained 🔐
- `DEPLOYMENT_CHECKLIST.md` - Complete testing checklist ✅

### Configuration Files (Auto-Created)
- `.gitignore` - Exclude secrets & build files
- `render.yaml` - Backend deployment config
- `vercel.json` - Frontend deployment config
- `.env.example` & `frontend/.env.example` - Environment templates

### Helper Scripts
- `deploy.ps1` - Git initialization helper (Windows)

---

## 🎯 High-Level Process

```
┌─────────────────────────────────────────────────────┐
│ 1. Push to GitHub (2 min)                           │
│    - git init, commit, push                         │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│ 2. Deploy Backend on Render (5 min)                 │
│    - Create service                                 │
│    - Add environment variables                      │
│    - Get Render URL                                 │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│ 3. Deploy Frontend on Vercel (5 min)                │
│    - Import repository                              │
│    - Add VITE_API_URL (use Render URL)              │
│    - Get Vercel URL                                 │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│ 4. Update Backend CORS (1 min)                      │
│    - Add Vercel URL to CORS_ORIGINS                 │
│    - Render auto-redeploys                          │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│ 5. Test Your App (2 min)                            │
│    - Login, create doc, upload file, share          │
│    - ✅ Success! Your app is live!                  │
└─────────────────────────────────────────────────────┘
```

---

## 🔑 Key URLs After Deployment

After completing the steps, you'll have:

```
Frontend:    https://YOUR_VERCEL_URL          (your app)
Backend:     https://YOUR_RENDER_URL/docs     (API docs)
GitHub:      https://github.com/YOUR_USERNAME/ajaia-docs
```

---

## ⚠️ Important Before You Start

✅ You have a GitHub account  
✅ You have a Render account (free)  
✅ You have a Vercel account (free)  
✅ All files are configured and ready  

**Not done yet?**
- GitHub: https://github.com (free, takes 2 min)
- Render: https://render.com (free, sign in with GitHub)
- Vercel: https://vercel.com (free, sign in with GitHub)

---

## 🆘 Having Issues?

### Before Deployment
- Read the guide you chose above
- Check `.env.example` files are filled correctly
- Verify accounts are created

### During Deployment
- Check step 2-4 in your chosen guide
- See troubleshooting in `DEPLOYMENT_CHECKLIST.md`

### After Deployment
- Login with demo accounts (Alice/Bob/Carol, password: password123)
- Test basic features (create, edit, share)
- Check browser console (F12) for errors
- See troubleshooting matrix in `DEPLOYMENT_CHECKLIST.md`

---

## ✨ Features After Deployment

Your live app will have:

✅ Multiple document types (.docx, .md, .txt)  
✅ Real-time editing with autosave  
✅ Document sharing with permissions  
✅ File import (txt, md, docx)  
✅ Multi-tab login support  
✅ Rich text formatting  
✅ Table support (.docx only)  
✅ XSS protection & sanitization  
✅ Duplicate filename prevention  
✅ 50+ automated tests  

---

## 📊 What Gets Deployed

### Frontend (Vercel)
- React app with Vite
- Your browser gets the UI
- Auto-updates on git push

### Backend (Render)
- FastAPI server
- Runs your API
- SQLite database included

### Database
- SQLite: Simple, free, but resets on restart
- (Upgrade to PostgreSQL later if needed)

---

## 🎓 Learning Resources

**Stuck? Read these:**
- `DEPLOYMENT_CHECKLIST.md` - Troubleshooting matrix
- `ENV_SETUP.md` - Environment variable help
- `QUICKSTART_DEPLOY.md` - Quick reference

**Still stuck? Check:**
- Render docs: https://render.com/docs
- Vercel docs: https://vercel.com/docs
- FastAPI docs: https://fastapi.tiangolo.com

---

## ✅ Deployment Checklist (Quick)

- [ ] Read your chosen guide
- [ ] Create accounts (GitHub, Render, Vercel)
- [ ] Push code to GitHub
- [ ] Deploy backend on Render
- [ ] Deploy frontend on Vercel
- [ ] Update CORS configuration
- [ ] Test your app
- [ ] Share with users! 🎉

---

## 🚀 Ready?

Pick your path above and start deploying!

### Fast: ~15 minutes
➡️ **[QUICKSTART_DEPLOY.md](QUICKSTART_DEPLOY.md)**

### Detailed: ~30 minutes
➡️ **[DEPLOYMENT.md](DEPLOYMENT.md)**

### Complete: ~1 hour
➡️ **[DEPLOYMENT_COMPLETE.md](DEPLOYMENT_COMPLETE.md)**

---

## 💡 Pro Tips

1. **Bookmark your URLs** after deployment
2. **Share frontend URL** with users (not backend)
3. **Monitor logs** first few days
4. **Test on free tier** first
5. **Upgrade later** if you need more resources

---

## Questions?

All answers are in the deployment guides!

**Not in the guides?** Check:
- Browser console for errors (F12)
- Service logs (Render/Vercel dashboard)
- Troubleshooting matrix in `DEPLOYMENT_CHECKLIST.md`

---

## You've Got This! 💪

Your app is configured, documented, and ready to deploy.

**Choose a guide above and get started!**

Questions about anything? The guides have you covered.

**Let's go! 🚀**
