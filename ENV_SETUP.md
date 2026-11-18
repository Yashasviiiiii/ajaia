# Environment Variables Setup Guide

## Overview

Environment variables are used to configure the app for different environments (development, staging, production).

---

## Local Development Setup

### Backend (.env)

1. Create `backend/.env` from template:
```bash
cp backend\.env.example backend\.env
```

2. Edit `backend/.env`:
```env
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=dev-secret-key-12345
CORS_ORIGINS=http://localhost:5173
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
FRONTEND_URL=http://localhost:5173
```

### Frontend (.env.local)

1. Create `frontend/.env.local` from template:
```bash
cp frontend\.env.example frontend\.env.local
```

2. Edit `frontend/.env.local`:
```env
VITE_API_URL=http://localhost:8000
VITE_DEBUG=true
```

---

## Production Setup (Render + Vercel)

### Backend on Render

Environment variables are set in the Render dashboard.

#### Required Variables:

**SECRET_KEY** (CRITICAL)
- Generate a secure key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
- Copy the output and paste into Render
- Example: `FjK8_9xL2pQ4mN7vB3cD5eF6gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6`

**DATABASE_URL**
- For SQLite (free tier): `sqlite:///./app.db`
- For PostgreSQL (production):
  ```
  postgresql://user:password@host:5432/database_name
  ```
  Get the full URL from Render PostgreSQL service

**CORS_ORIGINS**
- Add your Vercel frontend URL:
  ```
  http://localhost:5173,https://YOUR_VERCEL_URL
  ```
- Replace `YOUR_VERCEL_URL` with your actual Vercel domain

**ENVIRONMENT**
- Set to: `production`

**Other Variables**
```
API_HOST=0.0.0.0
API_PORT=$PORT (use Render's default)
API_RELOAD=false
DEBUG=false
FRONTEND_URL=https://YOUR_VERCEL_URL
```

### Frontend on Vercel

Environment variables are set in the Vercel dashboard.

#### Required Variables:

**VITE_API_URL**
- Set to your Render backend URL:
  ```
  https://YOUR_RENDER_URL
  ```
- Example: `https://ajaia-docs-api.onrender.com`
- Make sure this is set for Production, Preview, AND Development environments

**VITE_DEBUG**
- Set to: `false`

---

## How to Set Environment Variables

### Render

1. Go to your service in Render dashboard
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Enter:
   - **Key:** Variable name (e.g., `SECRET_KEY`)
   - **Value:** The value
   - Select environment scope
5. Click **"Save"**
6. Your service will automatically redeploy with new variables

### Vercel

1. Go to your project in Vercel dashboard
2. Click **"Settings"** → **"Environment Variables"**
3. Click **"Add New"**
4. Enter:
   - **Name:** Variable name (e.g., `VITE_API_URL`)
   - **Value:** The value
5. Select environments:
   - ☑️ Production
   - ☑️ Preview
   - ☑️ Development
6. Click **"Save"**
7. Redeploy to apply changes (or just commit/push)

---

## Environment-Specific Examples

### Development (Local)

**Backend**
```env
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=dev-key-for-testing
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
FRONTEND_URL=http://localhost:5173
```

**Frontend**
```env
VITE_API_URL=http://localhost:8000
VITE_DEBUG=true
```

### Staging (Demo on Cloud)

**Backend**
```env
ENVIRONMENT=staging
DEBUG=false
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=<generate-secure-key>
CORS_ORIGINS=http://localhost:5173,https://staging-ajaia-docs.vercel.app
API_HOST=0.0.0.0
API_PORT=$PORT
API_RELOAD=false
FRONTEND_URL=https://staging-ajaia-docs.vercel.app
```

**Frontend**
```env
VITE_API_URL=https://ajaia-docs-api.onrender.com
VITE_DEBUG=false
```

### Production

**Backend**
```env
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://user:password@db.host:5432/db_name
SECRET_KEY=<generate-secure-key>
CORS_ORIGINS=https://ajaia-docs.vercel.app
API_HOST=0.0.0.0
API_PORT=$PORT
API_RELOAD=false
FRONTEND_URL=https://ajaia-docs.vercel.app
```

**Frontend**
```env
VITE_API_URL=https://api.ajaia-docs.com
VITE_DEBUG=false
```

---

## Secret Generation

### Generate SECRET_KEY

**Command Line:**
```bash
# Option 1: Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Option 2: OpenSSL
openssl rand -base64 32

# Option 3: Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

**Online Tool:** https://randomkeygen.com/ (256-bit WPA Passphrase)

### Never Commit .env Files

These files contain secrets and should never be committed to git.

1. `.gitignore` already excludes them:
   ```
   .env
   .env.local
   .env.*.local
   ```

2. Use `.env.example` to show what variables are needed

3. Team members copy `.env.example` → `.env` and fill in their own secrets

---

## Troubleshooting

### "Invalid API URL" on Frontend

**Problem:** Frontend can't reach backend
**Solution:**
- Check `VITE_API_URL` is set correctly
- Verify backend is running/deployed
- Check CORS is configured for frontend URL

### "Connection refused" on Backend

**Problem:** Backend can't connect to database
**Solution:**
- Check `DATABASE_URL` is correct
- For Postgres: verify host/port/credentials
- For SQLite: verify file path is writable

### "SECRET_KEY not found" on Backend

**Problem:** Backend starts but JWT fails
**Solution:**
- Add `SECRET_KEY` to environment variables
- Restart the service after adding

### Vercel Deploy Fails

**Problem:** Build fails with env variable error
**Solution:**
- Check environment variables are set for "Production"
- Trigger a new deployment after setting variables
- Check variable names match (case-sensitive)

### CORS Error in Browser

**Problem:** Frontend gets 403 from backend
**Solution:**
- Update `CORS_ORIGINS` to include frontend URL
- Remove trailing slashes: ✅ `https://example.com` ❌ `https://example.com/`
- Redeploy backend after change

---

## Security Best Practices

1. **Use strong SECRET_KEY**
   - At least 32 characters
   - Random, not predictable
   - Different for each environment

2. **Never hardcode secrets**
   - Always use environment variables
   - Never commit .env files
   - Rotate keys periodically

3. **Limit CORS origins**
   - Only allow your frontend domain
   - Don't use wildcards in production
   - Review for each deployment

4. **Use HTTPS everywhere**
   - Render and Vercel use HTTPS by default
   - Update API URLs to use `https://`

5. **Audit environment variables**
   - Regularly check what's set
   - Remove unused variables
   - Update when rotating secrets

---

## Quick Checklist

- [ ] Created `.env` from `.env.example` (local)
- [ ] Created `.env.local` from `.env.example` (local)
- [ ] Generated secure `SECRET_KEY`
- [ ] Set backend environment variables on Render
- [ ] Set frontend environment variables on Vercel
- [ ] Updated `VITE_API_URL` with Render backend URL
- [ ] Updated `CORS_ORIGINS` with Vercel frontend URL
- [ ] Tested API connectivity
- [ ] Verified login works
- [ ] Checked browser console for errors
