# Deployment Checklist & Testing Guide

Complete this checklist to ensure your deployment is successful.

---

## Pre-Deployment Checklist

### Code Quality
- [ ] All tests pass locally: `pytest`
- [ ] No console errors: `npm run dev` (frontend)
- [ ] No backend errors: `uvicorn app.main:app --reload` (backend)
- [ ] Code committed to GitHub
- [ ] No uncommitted `.env` files

### Configuration
- [ ] `.gitignore` includes `.env` and `app.db`
- [ ] `render.yaml` configured correctly
- [ ] `vercel.json` configured correctly
- [ ] `.env.example` files created for documentation
- [ ] CORS origins updated in backend

### Security
- [ ] `SECRET_KEY` is strong (32+ chars, random)
- [ ] No hardcoded secrets in code
- [ ] `DEBUG=false` for production
- [ ] HTTPS enforced (automatic on Render/Vercel)

---

## GitHub Setup

- [ ] GitHub account created
- [ ] Repository `ajaia-docs` created
- [ ] Code pushed to `main` branch
- [ ] Verify on GitHub: https://github.com/YOUR_USERNAME/ajaia-docs
- [ ] Render/Vercel authorized to access GitHub

---

## Render Backend Deployment

### Service Creation
- [ ] Render account created with GitHub login
- [ ] New Web Service created from `ajaia-docs` repository
- [ ] Service name: `ajaia-docs-api`
- [ ] Environment: `Python 3`
- [ ] Region: `Oregon` (or your preference)
- [ ] Plan: Free tier (or paid)

### Build Configuration
- [ ] Build command: `cd backend && pip install -r requirements.txt`
- [ ] Start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Python version: `3.11.0`

### Environment Variables (All Scopes: All)
- [ ] `SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] `DATABASE_URL`: `sqlite:///./app.db` (or PostgreSQL URL)
- [ ] `CORS_ORIGINS`: `http://localhost:5173,https://YOUR_VERCEL_URL`
- [ ] `ENVIRONMENT`: `production`
- [ ] `DEBUG`: `false`

### Deployment Verification
- [ ] Build succeeds (check Render logs)
- [ ] Service starts without errors
- [ ] API docs accessible: `https://YOUR_RENDER_URL/docs`
- [ ] Note your Render URL (e.g., `https://ajaia-docs-api.onrender.com`)

---

## Vercel Frontend Deployment

### Project Setup
- [ ] Vercel account created with GitHub login
- [ ] Repository imported from GitHub
- [ ] Framework: `Vite`
- [ ] Root directory: `frontend`
- [ ] Build command: `npm run build`
- [ ] Output directory: `dist`

### Environment Variables
- [ ] Go to Settings → Environment Variables
- [ ] Add `VITE_API_URL`:
  - **Name**: `VITE_API_URL`
  - **Value**: `https://YOUR_RENDER_URL` (from Render step)
  - **Environments**: ☑️ Production, ☑️ Preview, ☑️ Development
- [ ] Click "Save"
- [ ] Trigger new deployment (or commit/push to main)

### Deployment Verification
- [ ] Build succeeds (check Vercel build logs)
- [ ] Frontend loads: `https://YOUR_VERCEL_URL`
- [ ] Note your Vercel URL (e.g., `https://ajaia-docs.vercel.app`)

### Update Backend CORS
- [ ] Go back to Render backend service
- [ ] Update `CORS_ORIGINS` to: `https://YOUR_VERCEL_URL`
- [ ] Service will redeploy automatically
- [ ] Wait for redeployment to complete

---

## Integration Testing

### Login Test
1. [ ] Open frontend: `https://YOUR_VERCEL_URL`
2. [ ] See login page with demo account buttons
3. [ ] Click "Alice" to fill email field
4. [ ] Password field auto-fills with `password123`
5. [ ] Click "Sign in"
6. [ ] Verify you're logged in (see "Alice" in header with "This Tab" badge)

### Document Creation Test
1. [ ] Click "+ New document"
2. [ ] Select "Word Document (.docx)"
3. [ ] See document created with title "Untitled.docx"
4. [ ] File type badge shows "DOCX"

### Edit & Autosave Test
1. [ ] Edit document title to "My First Doc"
2. [ ] Click away to trigger blur
3. [ ] Watch status change to "Saving..." → "All changes saved"
4. [ ] Refresh page
5. [ ] Verify title persisted
6. [ ] Add content to document
7. [ ] Watch autosave indicator

### File Upload Test
1. [ ] Create a test file locally:
   ```
   # My Test Doc
   This is a markdown file.
   
   ## Section 2
   - List item 1
   - List item 2
   ```
2. [ ] Save as `test.md`
3. [ ] Click "Upload file"
4. [ ] Select `test.md`
5. [ ] Verify document imported with:
   - Title: `test.md`
   - Badge shows: `MD`
   - Content shows formatted markdown

### Sharing Test (Multi-Tab)
1. [ ] Open new browser tab (separate session)
2. [ ] Login as Bob: `bob@example.com` / `password123`
3. [ ] You now have two tabs: Alice (Tab 1) and Bob (Tab 2)
4. [ ] Go back to Tab 1 (Alice)
5. [ ] Click "Share" on "My First Doc"
6. [ ] Select "Bob" with "Can edit"
7. [ ] Click "Share"
8. [ ] Go to Tab 2 (Bob)
9. [ ] Verify document appears under "Shared with me"
10. [ ] Click to open
11. [ ] Verify Bob can edit (toolbar visible, can type)
12. [ ] Go back to Tab 1
13. [ ] Change Bob's permission to "View only"
14. [ ] Go to Tab 2 (Bob)
15. [ ] Refresh page
16. [ ] Verify toolbar is hidden (read-only)
17. [ ] Try to edit (should not work)

### Permission Test
1. [ ] Stay as Bob (Tab 2)
2. [ ] Go back to Tab 1 as Alice
3. [ ] Create another document: "Private.docx"
4. [ ] Go to Tab 2 (Bob)
5. [ ] Verify Bob CANNOT see "Private.docx"
6. [ ] Manually try to access via URL: `https://YOUR_VERCEL_URL/docs/999`
7. [ ] Verify Bob sees "Not found" error (not "Permission denied")

### Multi-Document Type Test
1. [ ] Create each document type and verify:
   - [ ] Word (.docx): Table button visible
   - [ ] Markdown (.md): No table button
   - [ ] Plain Text (.txt): No table button
2. [ ] Edit .docx document
3. [ ] Insert a table (should work)
4. [ ] Edit .md document
5. [ ] Try to insert a table (button not available)

---

## Performance & Monitoring

### Backend Health
- [ ] Visit `https://YOUR_RENDER_URL/docs`
- [ ] API interactive docs load
- [ ] Try a GET `/api/users` (should return list)
- [ ] Check Render logs for errors
- [ ] Monitor CPU/Memory usage in Render

### Frontend Performance
- [ ] Page loads in < 3 seconds
- [ ] No 404 errors in Network tab
- [ ] No console errors (F12)
- [ ] All images/assets load
- [ ] Check Vercel Analytics (if available)

### Database
- [ ] Documents persist after refresh
- [ ] Shares persist after refresh
- [ ] No data loss on service restart

---

## Troubleshooting Matrix

| Issue | Symptom | Solution |
|-------|---------|----------|
| API not found | "Failed to fetch" in console | Check `VITE_API_URL` in Vercel |
| CORS error | "Access-Control-Allow-Origin" error | Update `CORS_ORIGINS` in Render |
| Login fails | 401 error, invalid credentials | Check `SECRET_KEY` matches |
| File upload fails | 413 or 422 error | File too large or wrong format |
| Documents don't save | No autosave indicator | Check database connectivity |
| Table button missing | Not visible on .docx docs | Check `file_extension` field |
| Multi-tab doesn't work | Login affects other tabs | Check sessionStorage vs localStorage |

---

## Rollback Procedures

### If Frontend Breaks
1. Go to Vercel dashboard → Deployments
2. Find last working deployment
3. Click → "Promote to Production"
4. App reverts to previous version

### If Backend Breaks
1. Go to Render dashboard → your service
2. Click "Manual Deploy" → "Redeploy Latest Commit"
3. Or push a fix to GitHub (auto-redeploy)

### If Database Corrupts
1. For SQLite: Delete `app.db` file
2. Render will recreate on restart
3. Data will be lost (use this only in emergencies!)

---

## Post-Deployment Tasks

- [ ] Announce deployment to team
- [ ] Share frontend URL: `https://YOUR_VERCEL_URL`
- [ ] Document API URL: `https://YOUR_RENDER_URL/docs`
- [ ] Set up monitoring alerts
- [ ] Schedule regular backups (if using Postgres)
- [ ] Monitor error logs daily for first week
- [ ] Collect user feedback

---

## Success Criteria

✅ All tests pass  
✅ Login works with demo accounts  
✅ Documents create and save  
✅ File upload works  
✅ Sharing works with correct permissions  
✅ Multi-tab sessions independent  
✅ File type badges display  
✅ Autosave works  
✅ No console errors  
✅ API docs accessible  

---

## Emergency Contacts & Resources

**Need Help?**
- Render Support: https://render.com/support
- Vercel Support: https://vercel.com/support
- GitHub Issues: Create in your repo
- FastAPI Docs: https://fastapi.tiangolo.com
- React Docs: https://react.dev

**Useful Commands:**

```bash
# Test backend locally
cd backend
source .venv/bin/activate
pytest
uvicorn app.main:app --reload

# Test frontend locally
cd frontend
npm run dev
npm run build

# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Check git status before pushing
git status
git log --oneline -5
```

---

## Completion

- [ ] All tests passed
- [ ] Frontend is live and working
- [ ] Backend is live and working
- [ ] Integration tests completed
- [ ] Rollback procedure understood
- [ ] Ready for production use! 🎉
