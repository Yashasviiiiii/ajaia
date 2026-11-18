# Manual Deployment Guide

Deploy manually to GitHub, Vercel (frontend), and Render (backend).

---

## Step 1: GitHub Setup

### Initialize Git Repository
```bash
cd c:\Users\chronos\Desktop\ajaia-docs
git init
git add .
git commit -m "Initial commit: Collaborative document editor"
```

### Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `ajaia-docs`
3. Description: `Collaborative document editor with real-time editing and sharing`
4. **Do NOT** initialize with README, .gitignore, or license
5. Click **Create repository**

### Push Code to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/ajaia-docs.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

**Verify:** Visit https://github.com/YOUR_USERNAME/ajaia-docs - you should see your code

---

## Step 2: Deploy Backend on Render

### 1. Create Render Account
- Go to https://render.com
- Click **Sign up**
- Select **Continue with GitHub**
- Authorize Render to access your GitHub account

### 2. Create Backend Service
1. Click **Dashboard**
2. Click **New** → **Web Service**
3. Click **Connect** on your `ajaia-docs` repository
4. Fill in deployment settings:
   - **Name:** `ajaia-docs-api`
   - **Environment:** `Python 3`
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Region:** `Oregon`
   - **Plan:** `Free`
5. Click **Create Web Service**

### 3. Add Environment Variables
In the Render dashboard for your service:

1. Go to **Environment** tab
2. Click **Add Environment Variable** for each:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `CORS_ORIGINS` | `http://localhost:5173` (update later after Vercel deploy) |
| `ENVIRONMENT` | `production` |
| `DEBUG` | `false` |

3. Click **Save** after adding each variable

### 4. Wait for Deployment
- Render will start building
- Watch the logs (should take 2-3 minutes)
- When complete, you'll see a service URL

**Note your Render URL:** Looks like `https://ajaia-docs-api.onrender.com`

**Verify:** Visit `https://YOUR_RENDER_URL/docs` - should show API documentation

---

## Step 3: Deploy Frontend on Vercel

### 1. Create Vercel Account
- Go to https://vercel.com
- Click **Sign up**
- Select **Continue with GitHub**
- Authorize Vercel to access your GitHub account

### 2. Import Project
1. Click **Dashboard**
2. Click **Add New...** → **Project**
3. Find your `ajaia-docs` repository and click **Import**
4. Configure project:
   - **Framework Preset:** `Vite`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Click **Deploy**

### 3. Wait for Deployment
- Vercel will build your frontend
- Should take 1-2 minutes
- When complete, you'll see a preview URL

**Note your Vercel URL:** Looks like `https://ajaia-docs.vercel.app`

**Verify:** Visit your Vercel URL - you should see the login page

---

## Step 4: Connect Frontend to Backend

### 1. Add Environment Variable to Vercel

1. Go to Vercel dashboard → Select your project
2. Click **Settings** → **Environment Variables**
3. Click **Add New**
4. Fill in:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://YOUR_RENDER_URL` (from Step 2)
   - **Environments:** Select **Production**, **Preview**, and **Development**
5. Click **Save**

### 2. Redeploy Frontend
1. Click **Deployments**
2. Select the most recent deployment
3. Click the **... menu** → **Redeploy**
4. Wait for redeploy (1-2 minutes)

**Test:** Visit your Vercel URL - login should work if backend connection is correct

---

## Step 5: Update Backend CORS

### 1. Update CORS in Render

1. Go to Render dashboard → Select your backend service
2. Click **Environment** tab
3. Find `CORS_ORIGINS` and click **Edit**
4. Change value from `http://localhost:5173` to `https://YOUR_VERCEL_URL` (from Step 3)
5. Click **Save**

### 2. Wait for Redeployment
- Render will automatically redeploy with new CORS settings
- Watch logs to confirm deployment completes

**Verify:** Try logging in from your Vercel URL - should work without CORS errors

---

## Testing Your Deployment

### 1. Login Test
```
Frontend URL: https://YOUR_VERCEL_URL
Email: alice@example.com
Password: password123
```

### 2. Create Document
1. Click **+ New document**
2. Select **Word Document (.docx)**
3. See document created
4. Check autosave indicator

### 3. Test File Upload
1. Create a test file: `test.md`
   ```markdown
   # Test Document
   This is a test.
   ```
2. Click **Upload file**
3. Select your test.md
4. Verify it imports correctly

### 4. Test Sharing
1. Open new browser tab (logged out)
2. Login as Bob: `bob@example.com` / `password123`
3. Go back to first tab (as Alice)
4. Click **Share** on your document
5. Select **Bob** → **Can edit** → **Share**
6. Go to Bob's tab
7. Refresh - document should appear under "Shared with me"

### 5. Check API Docs
Visit: `https://YOUR_RENDER_URL/docs`
Should show interactive API documentation

---

## Useful URLs

| Service | URL |
|---------|-----|
| Frontend (Vercel) | `https://YOUR_VERCEL_URL` |
| Backend (Render) | `https://YOUR_RENDER_URL` |
| API Docs | `https://YOUR_RENDER_URL/docs` |
| GitHub Repository | `https://github.com/YOUR_USERNAME/ajaia-docs` |

---

## Troubleshooting

### Frontend Shows "Failed to fetch"
**Problem:** Can't connect to backend
**Solution:**
1. Verify `VITE_API_URL` is set in Vercel environment variables
2. Verify Render backend is running (visit /docs endpoint)
3. Trigger Vercel redeploy after setting environment variable

### Get CORS Error
**Problem:** Browser blocks request
**Solution:**
1. Go to Render environment variables
2. Update `CORS_ORIGINS` with exact Vercel URL
3. Wait for Render to redeploy
4. Don't forget `https://` prefix!

### Login Doesn't Work
**Problem:** Invalid credentials
**Solution:**
1. Email must be exact: `alice@example.com` (not alice)
2. Password is always: `password123`
3. Check browser console (F12) for actual error message

### File Upload Fails
**Problem:** 413 or 422 error
**Solution:**
- File too large: Max 5MB
- Wrong format: Only .txt, .md, .docx supported
- Try a simple .txt file first

---

## Demo Accounts

All use password: `password123`

- alice@example.com
- bob@example.com
- carol@example.com

---

## Quick Reference: Environment Variables

**Backend (Render):**
```
SECRET_KEY=<generate-secure-key>
CORS_ORIGINS=https://YOUR_VERCEL_URL
ENVIRONMENT=production
DEBUG=false
```

**Frontend (Vercel):**
```
VITE_API_URL=https://YOUR_RENDER_URL
```

---

## Files Used for Deployment

**Backend:**
- `backend/requirements.txt` - Python dependencies
- `backend/app/main.py` - FastAPI application
- `render.yaml` - Render configuration (optional, not needed for manual deploy)

**Frontend:**
- `frontend/package.json` - Node dependencies
- `frontend/src/**` - React components
- `vercel.json` - Vercel configuration (optional, not needed for manual deploy)

**Configuration:**
- `.env.example` - Environment variable template (reference only)
- `.gitignore` - What git ignores

---

## After Deployment

1. **Share your app:**
   - Frontend URL to users: `https://YOUR_VERCEL_URL`
   - API docs to developers: `https://YOUR_RENDER_URL/docs`

2. **Monitor logs:**
   - Check Render logs daily for first week
   - Check Vercel build logs if deploys fail

3. **Plan next steps:**
   - Add custom domain (optional)
   - Upgrade to paid tier if needed (optional)
   - Set up database backups if using Postgres (optional)

---

## Success! 🎉

Your app is now live!

- **Users visit:** `https://YOUR_VERCEL_URL`
- **API available at:** `https://YOUR_RENDER_URL`
- **Code backed up:** `https://github.com/YOUR_USERNAME/ajaia-docs`

Congratulations on launching your collaborative document editor! 🚀
