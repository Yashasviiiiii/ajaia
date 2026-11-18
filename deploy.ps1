# Deployment Helper Script - PowerShell
# This script sets up Git and guides you through deployment

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Ajaia Docs - Deployment Helper" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Git found" -ForegroundColor Green
Write-Host ""

# Check if git is already initialized
if (Test-Path ".git") {
    Write-Host "⚠️  Git repository already initialized" -ForegroundColor Yellow
    Write-Host "Skipping git init" -ForegroundColor Yellow
} else {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Cyan
    git init
    Write-Host "✅ Repository initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "📝 Staging files..." -ForegroundColor Cyan
git add .
Write-Host "✅ Files staged" -ForegroundColor Green

Write-Host ""
Write-Host "💾 Creating initial commit..." -ForegroundColor Cyan
git commit -m "Initial commit: Collaborative document editor with tests and deployment configs"
Write-Host "✅ Commit created" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Next Steps" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "1️⃣  CREATE GITHUB REPOSITORY" -ForegroundColor Cyan
Write-Host "   • Go to: https://github.com/new" -ForegroundColor White
Write-Host "   • Repository name: ajaia-docs" -ForegroundColor White
Write-Host "   • Do NOT initialize with README/gitignore" -ForegroundColor White
Write-Host "   • Click 'Create repository'" -ForegroundColor White
Write-Host ""

Write-Host "2️⃣  PUSH TO GITHUB" -ForegroundColor Cyan
Write-Host "   Replace YOUR_USERNAME below, then run:" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/ajaia-docs.git" -ForegroundColor Green
Write-Host "   git branch -M main" -ForegroundColor Green
Write-Host "   git push -u origin main" -ForegroundColor Green
Write-Host ""

Write-Host "3️⃣  DEPLOY BACKEND (Render)" -ForegroundColor Cyan
Write-Host "   • Go to: https://render.com" -ForegroundColor White
Write-Host "   • Sign up with GitHub" -ForegroundColor White
Write-Host "   • Create new Web Service" -ForegroundColor White
Write-Host "   • Follow guide in DEPLOYMENT.md" -ForegroundColor White
Write-Host ""

Write-Host "4️⃣  DEPLOY FRONTEND (Vercel)" -ForegroundColor Cyan
Write-Host "   • Go to: https://vercel.com" -ForegroundColor White
Write-Host "   • Sign up with GitHub" -ForegroundColor White
Write-Host "   • Import the repository" -ForegroundColor White
Write-Host "   • Follow guide in DEPLOYMENT.md" -ForegroundColor White
Write-Host ""

Write-Host "📖 For detailed instructions, see: DEPLOYMENT.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "Questions? Check the README.md or DEPLOYMENT.md" -ForegroundColor Gray
