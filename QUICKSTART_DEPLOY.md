# Quick Start: Deploy to GitHub, Render & Vercel

Get your app live in 15 minutes!

---

## 1️⃣ Push to GitHub (2 min)

```bash
cd c:\Users\chronos\Desktop\ajaia-docs

# Initialize git
git init
git add .
git commit -m "Initial commit: Collaborative document editor"

# Create repository on https://github.com/new
# Repository name: ajaia-docs
# Do NOT initialize with README/gitignore

# Push code
git remote add origin https://github.com/YOUR_USERNAME/ajaia-docs.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## 2️⃣ Deploy Backend to Render (5 min)

### Step 1: Create Render Account
- Go to https://render.com
- Sign up with GitHub
- Authorize Render

### Step 2: Create Web Service
1. Click **"New+"** → **"Web Service"**
2. Connect your `ajaia-docs` repository
3. Fill in:
   - **Name:** `ajaia-docs-api`
   - **Environment:** Python 3
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

### Step 3: Add Environment Variables
1. Click **"Environment"** tab
2. Add these variables (Scope: All):

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `CORS_ORIGINS` | `http://localhost:5173` (will update later) |
| `ENVIRONMENT` | `production` |
| `DEBUG` | `false` |

3. Click **"Deploy"**
4. Wait 2-3 minutes for build ✅

**Note your Render URL** (e.g., `https://ajaia-docs-api.onrender.com`)

---

## 3️⃣ Deploy Frontend to Vercel (5 min)

### Step 1: Create Vercel Account
- Go to https://vercel.com
- Sign up with GitHub
- Authorize Vercel

### Step 2: Import Project
1. Click **"Add New"** → **"Project"**
2. Import `ajaia-docs` repository
3. Set:
   - **Framework:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

### Step 3: Add Environment Variable
1. Click **"Environment Variables"**
2. Add:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://YOUR_RENDER_URL` (from Render dashboard)
   - **Environments:** ☑️ Production, ☑️ Preview, ☑️ Development

3. Click **"Deploy"**
4. Wait 1-2 minutes for build ✅

**Note your Vercel URL** (e.g., `https://ajaia-docs.vercel.app`)

---

## 4️⃣ Update Backend CORS (1 min)

Go back to Render backend:

1. Click your service (`ajaia-docs-api`)
2. Click **"Environment"** tab
3. Edit `CORS_ORIGINS`:
   - Old: `http://localhost:5173`
   - New: `https://YOUR_VERCEL_URL` (from Vercel)
4. Click **"Save"**
5. Service auto-redeploys (wait 1 min)

---

## 5️⃣ Test (2 min)

### Open Frontend
Visit: `https://YOUR_VERCEL_URL`

### Login
- Click **"Alice"** button
- Password: `password123`
- Click **"Sign in"**

### Create Document
- Click **"+ New document"**
- Choose **"Word Document (.docx)"**
- Edit title: "Test Document"
- Type some content
- Watch "Saving..." → "All changes saved"

### Test Sharing
- Open another tab
- Login as **Bob**
- Go back to first tab
- Click **"Share"** on document
- Select **Bob** → **"Can edit"**
- Go to Bob's tab
- Refresh - document appears under "Shared with me"

### 🎉 Success!

---

## Useful URLs

| Service | URL |
|---------|-----|
| Frontend | `https://YOUR_VERCEL_URL` |
| Backend API | `https://YOUR_RENDER_URL/docs` |
| GitHub Repo | `https://github.com/YOUR_USERNAME/ajaia-docs` |

---

## Troubleshooting Quick Fixes

### "Failed to fetch" Error
**Problem:** Frontend can't reach backend
**Fix:**
1. Check `VITE_API_URL` in Vercel is correct
2. Visit backend URL to verify it's running
3. Trigger new Vercel deployment

### "CORS Error"
**Problem:** Browser blocks request
**Fix:**
1. Update `CORS_ORIGINS` in Render
2. Include your full Vercel URL (with `https://`)
3. Wait for Render to redeploy

### Login Doesn't Work
**Problem:** Invalid credentials
**Fix:**
1. Use exact demo emails: `alice@example.com`
2. Password is always: `password123`
3. Check browser console for errors

---

## Next Steps

1. Read `DEPLOYMENT_CHECKLIST.md` for comprehensive testing
2. Read `ENV_SETUP.md` for environment variable details
3. Read `DEPLOYMENT.md` for production considerations
4. Monitor your apps daily for first week
5. Set up database backups if needed

---

## Emergency Help

**Render Build Fails:**
- Check logs in Render dashboard
- Verify Python version
- Try redeploying

**Vercel Build Fails:**
- Check logs in Vercel dashboard
- Verify `VITE_API_URL` is set
- Try redeploying

**Both Working but Can't Connect:**
- Verify frontend can reach backend URL
- Check CORS configuration
- Verify environment variables

**Lost Data:**
- For SQLite: data is gone (rebuild only option)
- For Postgres: contact Render support

---

## Success! 🚀

Your app is live!
- Frontend: https://YOUR_VERCEL_URL
- Backend: https://YOUR_RENDER_URL

Share the frontend URL with users.
Use the backend `/docs` URL for API testing.
