# Deployment Guide

Deploy the app to GitHub, Render (backend), and Vercel (frontend).

## Step 1: Set Up GitHub Repository

### 1a. Initialize Git
```bash
cd c:\Users\chronos\Desktop\ajaia-docs
git init
git add .
git commit -m "Initial commit: Collaborative document editor"
```

### 1b. Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository named `ajaia-docs`
3. **Do NOT** initialize with README, .gitignore, or license (we already have these)
4. Click "Create repository"

### 1c. Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/ajaia-docs.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username.**

---

## Step 2: Deploy Backend to Render

### 2a. Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (easier for deployments)
3. Authorize Render to access your GitHub account

### 2b. Create Backend Service
1. Click **"New+"** → **"Web Service"**
2. Connect your GitHub repository (`ajaia-docs`)
3. Choose branch: `main`
4. Fill in:
   - **Name:** `ajaia-docs-api`
   - **Environment:** `Python 3`
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free tier (or paid if desired)
5. Click **"Create Web Service"**

### 2c. Add Environment Variables
In Render dashboard for your service:
1. Go to **Environment** tab
2. Add:
   - **SECRET_KEY:** Generate a random string (use `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
   - **DATABASE_URL:** Keep as `sqlite:///./app.db` (file-based for free tier)
   - **ENVIRONMENT:** `production`

3. Click **"Save"**

Your backend will deploy automatically. Wait for the build to complete (takes ~2-3 minutes).

**Note the service URL** (looks like `https://ajaia-docs-api.onrender.com`)

### 2d. Verify Backend
Once deployed, visit: `https://YOUR_RENDER_URL/docs` to see API documentation.

---

## Step 3: Deploy Frontend to Vercel

### 3a. Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub (easier for deployments)
3. Authorize Vercel to access your GitHub account

### 3b. Import Project
1. Click **"Add New..."** → **"Project"**
2. Import the `ajaia-docs` repository from GitHub
3. Framework preset: Select **"Vite"**
4. Root directory: `frontend`
5. Build command: `npm run build`
6. Output directory: `dist`

### 3c. Add Environment Variables
Before deploying:
1. Click **"Environment Variables"**
2. Add:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://YOUR_RENDER_URL` (the backend URL from Step 2d)
   - **Environments:** Select `Production`, `Preview`, `Development`

3. Click **"Add"**

### 3d. Deploy
Click **"Deploy"** and wait for the build to complete (takes ~1-2 minutes).

**Your frontend URL will appear** (looks like `https://ajaia-docs.vercel.app`)

---

## Step 4: Configure CORS

The backend needs to allow requests from the Vercel frontend.

### 4a. Update Backend CORS
Edit `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "https://YOUR_VERCEL_URL",  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Replace `YOUR_VERCEL_URL` with your actual Vercel URL.

### 4b. Commit and Push
```bash
git add backend/app/main.py
git commit -m "Configure CORS for Vercel deployment"
git push origin main
```

Render will automatically redeploy with the changes.

---

## Step 5: Test the Deployment

1. Open your Vercel frontend: `https://ajaia-docs.vercel.app`
2. Try logging in with demo accounts:
   - Email: `alice@example.com`
   - Password: `password123`
3. Create a document
4. Try uploading a file
5. Test sharing with other demo users
6. Try editing from different browser tabs

---

## Troubleshooting

### Frontend shows "Failed to connect to API"
- Check that `VITE_API_URL` is set correctly in Vercel
- Verify the backend URL is accessible
- Check Render service is running (visit `/docs` endpoint)

### Render build fails
- Check build logs in Render dashboard
- Ensure `requirements.txt` has all dependencies
- Verify Python version is 3.10+

### Login doesn't work
- Check browser console for errors (F12)
- Verify tokens are being stored in sessionStorage
- Check CORS configuration is correct

### Database issues
- SQLite data is lost when Render restarts
- For production, upgrade to Render PostgreSQL
- Or use a persistent volume in Render

---

## Production Considerations

### For Production (Beyond Free Tier)

1. **Use PostgreSQL instead of SQLite**
   - Create Render PostgreSQL database
   - Update `DATABASE_URL` in environment variables
   - Run migrations on first deployment

2. **Set up proper SECRET_KEY**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   Use this value in Render environment variables

3. **Enable HTTPS** (automatically done on Vercel/Render)

4. **Set up monitoring**
   - Enable email alerts in Render for deployment failures
   - Monitor backend logs regularly

5. **Database backups**
   - Enable automatic backups for PostgreSQL
   - Consider daily exports for critical data

---

## Useful Links

- **Render Documentation:** https://render.com/docs
- **Vercel Documentation:** https://vercel.com/docs
- **GitHub Help:** https://docs.github.com
- **Uvicorn Deployment:** https://www.uvicorn.org/#running-with-gunicorn
- **Vite Deployment:** https://vitejs.dev/guide/ssr.html#setting-up-the-dev-server

---

## Quick Reference

| Service | URL Pattern | Status |
|---------|-----------|--------|
| Backend (Render) | `https://ajaia-docs-api.onrender.com` | Check `/docs` |
| Frontend (Vercel) | `https://ajaia-docs.vercel.app` | Visit site |
| GitHub | `https://github.com/USERNAME/ajaia-docs` | Repository |

---

## Rollback

If something goes wrong:

### Render
1. Go to Render dashboard
2. Click your service
3. Click **"Manual Deploy"** → **"Redeploy Latest Commit"**
4. Or push a new commit to trigger automatic redeploy

### Vercel
1. Go to Vercel dashboard
2. Click your project
3. Go to **"Deployments"**
4. Click the previous successful deployment
5. Click **"Promote to Production"**
